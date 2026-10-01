from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import os
from threading import RLock
from time import monotonic
from typing import Any

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware

from app.redmine.client import RedmineClient
from app.redmine.collector import RedmineCollector
from app.domain.project_state import build_project_state
from app.metrics.project_metrics import calculate_project_metrics
from app.time_utils import app_timezone, days_until
from app.domain.statuses import is_active_status, is_done_status, is_pending_status
from app.intelligence.redmine_delivery import build_project_delivery, build_version_delivery
from app.intelligence.redmine_ai import analyze_redmine_snapshot
from app.reports.api_daily import archive_api_snapshot

app = FastAPI(title="PM Agent API", version="0.4.2")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[x.strip() for x in os.getenv("PM_AGENT_CORS_ORIGINS", "http://localhost:3200").split(",") if x.strip()],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

_CACHE: dict[str, dict[str, Any]] = {}
_CACHE_LOCK = RLock()
_CACHE_TTL = float(os.getenv("PM_AGENT_CACHE_SECONDS", "90"))
_INTELLIGENCE_CACHE: dict[str, dict[str, Any]] = {}


def collector_for(project_id: str) -> tuple[RedmineCollector, RedmineClient]:
    client = RedmineClient()
    collector = RedmineCollector(client, project_key=project_id)
    return collector, client


def serialize_issue(state, client: RedmineClient | None = None) -> dict:
    issue = state.issue
    codes = {signal.code for signal in state.signals}
    issue_id = issue.key.removeprefix("RM-")
    pending = is_pending_status(issue.status)
    done = is_done_status(issue.status)
    # Held/Pending is a workflow state, not a hot spot. Preserve raw signals for
    # deep inspection, but only expose actionable blocked/unassigned flags to UI.
    blocked = "BLOCKED" in codes and not pending
    unassigned = not done and not pending and not issue.assignee
    return {
        "key": issue.key,
        "id": issue_id,
        "subject": issue.summary,
        "status": issue.status,
        "assignee": issue.assignee,
        "priority": issue.priority,
        "type": issue.issue_type,
        "dueDate": issue.due_date,
        "updatedAt": issue.updated_at,
        "daysToDue": state.metrics.days_to_due,
        "daysSinceUpdate": state.metrics.days_since_update,
        "doneRatio": issue.done_ratio,
        "versionId": issue.fixed_version_id,
        "versionName": issue.fixed_version_name,
        "overdue": "OVERDUE" in codes,
        "nearDue": "NEAR_DUE" in codes,
        "blocked": blocked,
        "blocking": "BLOCKING_OTHERS" in codes,
        "stale": "STALE" in codes,
        "stuck": "STUCK" in codes,
        "unassigned": unassigned,
        "pending": pending,
        "done": done,
        "signals": sorted(codes),
        "redmineUrl": f"{client.base_url}/issues/{issue_id}" if client else None,
    }


def _version_base(version: dict) -> dict:
    due = version.get("due_date")
    return {
        "id": version.get("id"),
        "name": version.get("name") or str(version.get("id")),
        "status": version.get("status"),
        "dueDate": due,
        "daysLeft": days_until(due),
        "description": version.get("description") or "",
        "sharing": version.get("sharing"),
        "wikiPageTitle": version.get("wiki_page_title"),
    }


def _summary_from_issues(items: list[dict]) -> dict:
    total = len(items)
    done = sum(1 for x in items if x["done"])
    open_count = total - done
    overdue = sum(1 for x in items if x["overdue"])
    blocked = sum(1 for x in items if x["blocked"])
    stale = sum(1 for x in items if x["stale"])
    unassigned = sum(1 for x in items if x["unassigned"])
    near_due = sum(1 for x in items if x["nearDue"])
    pending = sum(1 for x in items if x.get("pending"))
    return {
        "total": total,
        "done": done,
        "open": open_count,
        "overdue": overdue,
        "blocked": blocked,
        "stale": stale,
        "unassigned": unassigned,
        "nearDue": near_due,
        "pending": pending,
        "progress": round((done / total) * 100) if total else 0,
    }


def _version_stats(versions: list[dict], issues: list[dict]) -> list[dict]:
    result: list[dict] = []
    for raw in versions:
        row = _version_base(raw)
        version_id = str(raw.get("id"))
        members = [x for x in issues if x.get("versionId") == version_id]
        row.update(_summary_from_issues(members))
        result.append(row)
    result.sort(key=lambda x: (x["dueDate"] is None, x["dueDate"] or "9999-12-31", str(x["name"])))
    return result


def _load_snapshot(project_id: str, refresh: bool = False) -> dict[str, Any]:
    now_mono = monotonic()
    if not refresh:
        with _CACHE_LOCK:
            cached = _CACHE.get(project_id)
            if cached and now_mono - cached["cachedAt"] < _CACHE_TTL:
                return cached

    collector, client = collector_for(project_id)
    project = client.get_project(project_id)
    state = build_project_state(collector, include_changelog=False)
    metrics = calculate_project_metrics(state)
    state.metrics = metrics
    issues = [serialize_issue(item, client) for item in state.issues]
    versions_raw = client.list_project_versions(project_id)
    versions = _version_stats(versions_raw, issues)
    synced_at = datetime.now(timezone.utc).isoformat()

    snapshot: dict[str, Any] = {
        "cachedAt": now_mono,
        "client": client,
        "project": project,
        "state": state,
        "metrics": metrics,
        "issues": issues,
        "versionsRaw": versions_raw,
        "versions": versions,
        "syncedAt": synced_at,
        "timezone": str(app_timezone()),
    }
    with _CACHE_LOCK:
        _CACHE[project_id] = snapshot
    return snapshot


def _version_status_closed(version: dict[str, Any]) -> bool:
    return str(version.get("status") or "").strip().lower() in {"closed", "done", "completed", "complete"}


def _classify_versions(versions: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any] | None, dict[str, Any] | None]:
    """Annotate lifecycle without treating an overdue open version as current.

    Current = nearest non-closed dated milestone from today onward.
    Next = the following dated milestone. No-deadline versions are Backlog.
    Closed versions stay visible for history.
    """
    future = [
        v for v in versions
        if not _version_status_closed(v)
        and v.get("dueDate") is not None
        and v.get("daysLeft") is not None
        and int(v["daysLeft"]) >= 0
    ]
    # Prefer a milestone that still has work; fall back to the nearest future one.
    active_future = [v for v in future if int(v.get("open") or 0) > 0]
    current = (active_future or future)[0] if (active_future or future) else None
    current_id = str(current.get("id")) if current else None
    current_pos = next((i for i, v in enumerate(future) if current_id and str(v.get("id")) == current_id), -1)
    next_version = future[current_pos + 1] if current_pos >= 0 and current_pos + 1 < len(future) else None
    next_id = str(next_version.get("id")) if next_version else None

    result: list[dict[str, Any]] = []
    for source in versions:
        v = dict(source)
        vid = str(v.get("id"))
        if _version_status_closed(v):
            phase = "CLOSED"
        elif v.get("dueDate") is None:
            phase = "BACKLOG"
        elif v.get("daysLeft") is not None and int(v["daysLeft"]) < 0:
            phase = "OVERDUE"
        elif vid == current_id:
            phase = "CURRENT"
        elif vid == next_id:
            phase = "NEXT"
        else:
            phase = "OPEN"
        v["phase"] = phase
        result.append(v)

    by_id = {str(v.get("id")): v for v in result}
    return result, by_id.get(current_id) if current_id else None, by_id.get(next_id) if next_id else None


def _filter_issues(items: list[dict], filter_type: str | None, version_id: str | None) -> list[dict]:
    result = items
    if version_id:
        result = [x for x in result if x.get("versionId") == str(version_id)]
    if not filter_type or filter_type == "all":
        return result
    predicates = {
        "overdue": lambda x: x["overdue"],
        "blocked": lambda x: x["blocked"],
        "stale": lambda x: x["stale"],
        "stuck": lambda x: x["stuck"],
        "unassigned": lambda x: x["unassigned"],
        "pending": lambda x: x.get("pending", False),
        "blocking": lambda x: x.get("blocking", False),
        "near_due": lambda x: x["nearDue"],
        "open": lambda x: not x["done"],
        "in_progress": lambda x: is_active_status(x.get("status")) and not x.get("done") and not x.get("pending"),
        "done": lambda x: x["done"],
    }
    predicate = predicates.get(filter_type)
    return [x for x in result if predicate(x)] if predicate else result


def _is_attention_issue(issue: dict[str, Any]) -> bool:
    # Pending/Held alone is informational. It only becomes hot when it is
    # overdue or blocks downstream work. Non-pending work keeps normal rules.
    if issue.get("pending"):
        return bool(issue.get("overdue") or issue.get("blocking"))
    return bool(issue.get("overdue") or issue.get("blocked") or issue.get("stale") or issue.get("unassigned") or issue.get("blocking"))


def _attention_sort_key(issue: dict[str, Any]):
    return (
        not issue.get("blocking", False),
        not issue.get("blocked", False),
        not issue.get("overdue", False),
        not issue.get("stale", False),
        not issue.get("unassigned", False),
        issue.get("dueDate") or "9999-12-31",
    )


@app.get("/health")
def health():
    return {"status": "ok", "source": "redmine", "version": app.version}


@app.get("/api/projects")
def projects():
    try:
        client = RedmineClient()
        items = client.list_projects()
        return {
            "items": [
                {
                    "id": item.get("id"),
                    "identifier": item.get("identifier") or str(item.get("id")),
                    "name": item.get("name") or item.get("identifier") or str(item.get("id")),
                    "description": item.get("description") or "",
                    "status": item.get("status"),
                    "createdOn": item.get("created_on"),
                    "updatedOn": item.get("updated_on"),
                    "parent": item.get("parent"),
                }
                for item in items
            ]
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Redmine project load failed: {type(exc).__name__}: {exc}") from exc


@app.get("/api/projects/{project_id}/overview")
def project_overview(project_id: str, refresh: bool = False):
    try:
        snapshot = _load_snapshot(project_id, refresh=refresh)
        metrics = snapshot["metrics"]
        issues = snapshot["issues"]
        versions, current_version, next_version = _classify_versions(snapshot["versions"])
        status_counts = Counter(item["status"] for item in issues)
        assignee_counts = Counter(item["assignee"] or "Chưa phân công" for item in issues if not item["done"] and not item.get("pending"))
        total = metrics.total_issues
        progress = round((metrics.done_issues / total) * 100) if total else 0
        attention = sorted([x for x in issues if _is_attention_issue(x)], key=_attention_sort_key)[:12]
        risk_summary, actions = build_project_delivery(issues, current_version, versions)
        health = risk_summary["level"]
        project = snapshot["project"]
        return {
            "project": {"id": project.get("id"), "identifier": project.get("identifier", project_id), "name": project.get("name", project_id), "description": project.get("description") or ""},
            "syncedAt": snapshot["syncedAt"],
            "timezone": snapshot["timezone"],
            "cacheSeconds": _CACHE_TTL,
            "health": health,
            "progress": progress,
            "metrics": metrics.model_dump() if hasattr(metrics, "model_dump") else metrics.__dict__,
            "currentVersion": current_version,
            "nextVersion": next_version,
            "versions": versions,
            "statusCounts": dict(status_counts),
            "assigneeCounts": dict(assignee_counts.most_common(10)),
            "attention": attention,
            "riskSummary": risk_summary,
            "actions": actions,
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Redmine analysis failed: {type(exc).__name__}: {exc}") from exc


@app.get("/api/projects/{project_id}/intelligence")
def project_intelligence(project_id: str, refresh: bool = False):
    """AI PM Intelligence over the cached Redmine snapshot.

    This endpoint is intentionally separate from /overview so dashboard loading
    remains fast even when an LLM provider is slow or unavailable.
    """
    try:
        snapshot = _load_snapshot(project_id, refresh=refresh)
        archive_api_snapshot(snapshot)
        cache_key = f"{project_id}:{snapshot['syncedAt']}"
        if not refresh:
            cached = _INTELLIGENCE_CACHE.get(cache_key)
            if cached:
                return cached

        versions, current_version, next_version = _classify_versions(snapshot["versions"])
        # Feed lifecycle annotation to the intelligence layer without mutating
        # the raw Redmine cache used by other requests.
        ai_snapshot = dict(snapshot)
        ai_snapshot["versions"] = versions
        risk_summary, actions = build_project_delivery(snapshot["issues"], current_version, versions)
        result = analyze_redmine_snapshot(ai_snapshot, current_version, next_version, risk_summary, actions)
        for key in list(_INTELLIGENCE_CACHE):
            if key.startswith(f"{project_id}:"):
                _INTELLIGENCE_CACHE.pop(key, None)
        _INTELLIGENCE_CACHE[cache_key] = result
        return result
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"PM Intelligence failed: {type(exc).__name__}: {exc}") from exc


@app.get("/api/projects/{project_id}/issues")
def project_issues(
    project_id: str,
    filter_type: str | None = Query(None, alias="filter"),
    version_id: str | None = Query(None, alias="versionId"),
    refresh: bool = False,
):
    try:
        snapshot = _load_snapshot(project_id, refresh=refresh)
        items = _filter_issues(snapshot["issues"], filter_type, version_id)
        project = snapshot["project"]
        versions, _, _ = _classify_versions(snapshot["versions"])
        return {
            "project": {"id": project.get("id"), "identifier": project.get("identifier", project_id), "name": project.get("name", project_id)},
            "syncedAt": snapshot["syncedAt"],
            "timezone": snapshot["timezone"],
            "filter": filter_type or "all",
            "versionId": version_id,
            "total": len(items),
            "items": items,
            "versions": versions,
        }
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Redmine issue load failed: {type(exc).__name__}: {exc}") from exc


@app.get("/api/projects/{project_id}/versions/{version_id}")
def project_version(project_id: str, version_id: str, refresh: bool = False):
    try:
        snapshot = _load_snapshot(project_id, refresh=refresh)
        versions, _, _ = _classify_versions(snapshot["versions"])
        version = next((v for v in versions if str(v.get("id")) == str(version_id)), None)
        if not version:
            raise HTTPException(status_code=404, detail="Redmine version not found")
        items = [x for x in snapshot["issues"] if x.get("versionId") == str(version_id)]
        status_counts = Counter(x["status"] for x in items)
        assignee_counts = Counter((x["assignee"] or "Chưa phân công") for x in items if not x["done"] and not x.get("pending"))
        attention = sorted([x for x in items if _is_attention_issue(x)], key=_attention_sort_key)
        risk_summary, actions = build_version_delivery(version, items)
        project = snapshot["project"]
        return {
            "project": {"id": project.get("id"), "identifier": project.get("identifier", project_id), "name": project.get("name", project_id)},
            "syncedAt": snapshot["syncedAt"],
            "timezone": snapshot["timezone"],
            "version": version,
            "statusCounts": dict(status_counts),
            "assigneeCounts": dict(assignee_counts.most_common(20)),
            "attention": attention,
            "issues": items,
            "riskSummary": risk_summary,
            "actions": actions,
        }
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Redmine version load failed: {type(exc).__name__}: {exc}") from exc


@app.get("/api/projects/{project_id}/daily-reports")
def project_daily_reports(project_id: str, filename: str | None = None):
    """Read archived daily reports without running the Telegram publisher."""
    from pathlib import Path
    from app.reports.archived_short import archived_short
    import re

    if not re.fullmatch(r"[A-Za-z0-9_-]+", project_id):
        raise HTTPException(status_code=400, detail="Invalid project identifier")
    try:
        identifier = project_id
        if project_id.isdigit():
            identifier = RedmineClient().get_project(project_id).get("identifier") or project_id
        root = Path(os.getenv("DAILY_REPORT_DIRECTORY", "data/daily_reports"))
        if not root.is_absolute():
            root = Path(__file__).resolve().parent.parent / root
        root = root.resolve()
        directory = (root / identifier).resolve()
        if directory.parent != root:
            raise HTTPException(status_code=400, detail="Invalid project identifier")
        files = sorted(
            (p for p in directory.glob("*.md") if "Daily_Report" in p.name and p.resolve().parent == directory),
            key=lambda p: ((re.search(r"\d{4}-\d{2}-\d{2}(?:_\d{6})?", p.name).group(0) if re.search(r"\d{4}-\d{2}-\d{2}(?:_\d{6})?", p.name) else ""), p.name), reverse=True,
        )
        items = []
        for report in files:
            date = re.search(r"\d{4}-\d{2}-\d{2}(?:_\d{6})?", report.name)
            text = report.read_text(encoding="utf-8")
            title = re.search(r"^# (.+)$", text, re.M)
            health = re.search(r"\*\*(?:Project Health|Health):\*\*\s*(.+)", text)
            items.append({"filename": report.name, "date": date.group(0) if date else None,
                          "title": title.group(1) if title else identifier,
                          "health": health.group(1).strip() if health else None,
                          "shortContent": archived_short(report, identifier, text)})
        selected = next((p for p in files if p.name == filename), None) if filename else None
        if filename and selected is None:
            raise HTTPException(status_code=404, detail="Không tìm thấy báo cáo ngày")
        return {"items": items, "report": {"filename": selected.name, "content": selected.read_text(encoding="utf-8")} if selected else None}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Không đọc được báo cáo ngày") from exc


@app.post("/api/projects/{project_id}/daily-reports")
def generate_project_daily_report(project_id: str):
    """Explicit refresh: collect Redmine, analyze with AI, save snapshot and reports."""
    import re
    if not re.fullmatch(r"[A-Za-z0-9_-]+", project_id):
        raise HTTPException(status_code=400, detail="Invalid project identifier")
    try:
        snapshot = _load_snapshot(project_id, refresh=True)
        filename = archive_api_snapshot(snapshot, include_ai=True)
        identifier = str(snapshot["project"].get("identifier") or project_id)
        result = project_daily_reports(identifier)
        result["generatedFilename"] = filename
        result["syncedAt"] = snapshot["syncedAt"]
        result["aiStatus"] = snapshot.get("dailyReportAiStatus")
        return result
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Không tạo được báo cáo ngày mới") from exc


from pydantic import BaseModel, Field
from typing import Literal

class ChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(min_length=1, max_length=5000)

class ProjectChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    history: list[ChatTurn] = Field(default_factory=list, max_length=8)

@app.post("/api/projects/{project_id}/chat")
def project_chat(project_id: str, request: ProjectChatRequest):
    from app.intelligence.project_chat import answer_project
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Nhập câu hỏi trước khi gửi")
    try:
        snapshot = _load_snapshot(project_id, refresh=False)
        versions, current, upcoming = _classify_versions(snapshot["versions"])
        context = dict(snapshot)
        context["versions"] = versions
        risk, actions = build_project_delivery(snapshot["issues"], current, versions)
        return answer_project(context, current, upcoming, risk, actions, request.message.strip(), [turn.model_dump() for turn in request.history])
    except Exception as exc:
        raise HTTPException(status_code=502, detail="Không tải được dữ liệu dự án cho chatbot") from exc
