from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo
import os

from app.i18n import health_label, is_vi, risk_label, trend_label
from app.intelligence.change_summary import build_change_summary
from app.intelligence.dependency_clusters import build_dependency_clusters
from app.intelligence.management_leverage import build_management_leverage
from app.reports.deterministic_brief import markdown_fallback_actions
from app.source_urls import issue_url, project_url, source_name


class DailyReportFileWriter:
    def __init__(self, directory: str = "data/daily_reports", retention: int = 14) -> None:
        self.directory=Path(directory); self.retention=retention

    def write(self,*,project_state,metrics,intelligence,delta,hotspots,risk_intelligence=None,ai_analysis=None,ai_error:str|None=None,jira_base_url:str,change_limit:int=12,cluster_limit:int=6)->Path:
        project_dir=self.directory/project_state.project_key; project_dir.mkdir(parents=True,exist_ok=True)
        tz_name=os.getenv("REPORT_TIMEZONE","Asia/Ho_Chi_Minh")
        try: now=datetime.now(ZoneInfo(tz_name))
        except Exception: now=datetime.now().astimezone()
        path=project_dir/f"{project_state.project_key}_Daily_Report_{now.strftime('%Y-%m-%d_%H%M%S%f')}.md"
        health=(ai_analysis.health if ai_analysis is not None else intelligence.health)
        title="Báo cáo dự án hằng ngày" if is_vi() else "Daily Project Report"
        captured="Thời điểm ghi nhận" if is_vi() else "Captured"
        health_t="Project Health" if is_vi() else "Health"
        lines=[f"# {title} — {project_state.project_key}","",f"**{captured}:** {now.isoformat()}",f"**{health_t}:** {health_label(health)}",""]
        lines.extend(_executive_section(ai_analysis,intelligence,project_state,metrics,hotspots,risk_intelligence))
        lines.extend(_snapshot_section(metrics,risk_intelligence))
        lines.extend(_risk_section(ai_analysis,hotspots,project_state,risk_intelligence,jira_base_url))
        lines.extend(_dependency_section(risk_intelligence,jira_base_url,cluster_limit))
        lines.extend(_dependency_hygiene_section(project_state,jira_base_url))
        lines.extend(_change_section(delta,jira_base_url,change_limit))
        lines.extend(_escalation_section(risk_intelligence,jira_base_url))
        lines.extend(_action_section(ai_analysis,project_state,hotspots,risk_intelligence,jira_base_url))
        lines.extend(_observation_section(ai_analysis,hotspots,risk_intelligence,jira_base_url))
        lines.extend(_hotspot_section(hotspots,jira_base_url))
        lines.extend(_evidence_section(project_state,jira_base_url))
        if ai_error:
            lines.extend(["## Trạng thái AI" if is_vi() else "## AI Availability","",("- AI tạm thời không khả dụng; báo cáo vẫn dùng deterministic intelligence đầy đủ." if is_vi() else "- AI temporarily unavailable; the report still uses full deterministic intelligence."),""])
        path.write_text("\n".join(lines).rstrip()+"\n",encoding="utf-8")
        self._prune(project_dir)
        return path

    def _prune(self,project_dir:Path)->None:
        if self.retention<=0:return
        files=sorted(project_dir.glob("*_Daily_Report_*.md"),key=lambda p:p.stat().st_mtime,reverse=True)
        for p in files[self.retention:]:
            try:
                p.unlink()
                p.with_suffix(".short.html").unlink(missing_ok=True)
            except OSError:pass


def _executive_section(ai,intelligence,project_state,metrics,hotspots,risk_intelligence):
    title="## Đánh giá tổng quan" if is_vi() else "## Executive Assessment"
    if ai and ai.summary:
        return [title,"",ai.summary,"",]
    clusters=build_dependency_clusters(risk_intelligence)
    critical=[h.issue_key for h in (hotspots.items if hotspots else []) if h.level=="CRITICAL"][:3]
    if is_vi():
        text=f"Dự án {project_state.project_key} đang ở mức {health_label(intelligence.health)}."
        if critical:text+=" Áp lực delivery tập trung ở "+", ".join(critical)+"."
        if clusters and clusters[0].affected_issue_keys:text+=f" Root dependency {clusters[0].root_issue_key} ảnh hưởng {len(clusters[0].affected_issue_keys)} issue downstream."
    else:
        text=f"Project {project_state.project_key} is {intelligence.health}."
        if critical:text+=" Delivery pressure is concentrated around "+", ".join(critical)+"."
    return [title,"",text,""]


def _snapshot_section(metrics,ri):
    completion=round(metrics.done_issues/metrics.total_issues*100) if metrics.total_issues else 0
    if is_vi():
        lines=["## Tổng quan dự án","",f"- Tổng issue: **{metrics.total_issues}**",f"- Đang hoạt động: **{metrics.active_issues}**",f"- Hoàn thành: **{metrics.done_issues}** ({completion}%)",f"- Quá hạn: **{metrics.overdue_issues}**",f"- Sắp đến hạn: **{metrics.near_due_issues}**",f"- Bị chặn: **{metrics.blocked_issues}**",f"- Blocker đang hoạt động: **{metrics.blocking_issues}**",f"- Issue mở chưa có owner: **{metrics.unassigned_issues}**"]
        if ri: lines.append(f"- Risk Pressure: **{ri.previous_project_score if ri.previous_project_score is not None else 'N/A'} → {ri.project_score}** ({trend_label(ri.project_trend)})")
    else:
        lines=["## Project Snapshot","",f"- Total issues: **{metrics.total_issues}**",f"- Active: **{metrics.active_issues}**",f"- Done: **{metrics.done_issues}** ({completion}%)",f"- Overdue: **{metrics.overdue_issues}**",f"- Near due: **{metrics.near_due_issues}**",f"- Blocked: **{metrics.blocked_issues}**",f"- Active blockers: **{metrics.blocking_issues}**",f"- Unassigned open issues: **{metrics.unassigned_issues}**"]
        if ri: lines.append(f"- Risk pressure: **{ri.previous_project_score if ri.previous_project_score is not None else 'N/A'} → {ri.project_score}** ({ri.project_trend})")
    return lines+[""]


def _issue_link(key,base): return f"[{key}]({issue_url(key, base)})"


def _is_done_state(st) -> bool:
    return bool(st and (st.issue.status or "").strip().lower() in {"done", "closed", "resolved"})


def _risk_section(ai,hotspots,project_state,ri,base):
    title="## Priority Risks"; lines=[title,""]
    states={s.issue.key:s for s in project_state.issues}
    ri_by={i.issue_key:i for i in ri.items} if ri else {}
    hotspot_by={h.issue_key:h for h in (hotspots.items if hotspots else [])}

    # AI owns risk selection/severity when available. Deterministic hotspots
    # remain a fallback and an audit hint, not the primary ranking authority.
    if ai and ai.risks:
        ranked=[(r.issue_key,r) for r in ai.risks[:6]]
    else:
        ranked=[(h.issue_key,None) for h in (hotspots.items[:6] if hotspots else [])]
    if not ranked:
        return lines+[("- Không có rủi ro đáng kể." if is_vi() else "- No material risks."),""]

    for key,air in ranked:
        st=states.get(key)
        if not st or _is_done_state(st):
            continue
        h=hotspot_by.get(key)
        lines.append(f"### {_issue_link(key,base)}")
        if air:
            lines.append(f"- **AI Delivery Risk:** {risk_label(air.level)}")
        if h:
            lines.append(f"- **Rule-based Hint:** {risk_label(h.level)} · pressure {h.score}")
        if air and air.impact:
            lines.extend(["",f"**Impact:** {air.impact}"])
        lines.extend(["","**Evidence:**"])
        codes={sig.code for sig in st.signals}
        if "OVERDUE" in codes and st.metrics.days_to_due is not None:
            lines.append(f"- {'Quá hạn' if is_vi() else 'Overdue'}: {abs(st.metrics.days_to_due)} {'ngày' if is_vi() else 'days'}")
        targets=[]
        blocked=[]
        for d in (st.issue.dependencies or []):
            related=states.get(d.related_issue_key)
            if not related or _is_done_state(related):
                continue
            relation=(d.relation or '').lower()
            if relation=='blocks' and "BLOCKING_OTHERS" in codes:
                targets.append(d.related_issue_key)
            elif 'blocked by' in relation and "BLOCKED" in codes:
                blocked.append(d.related_issue_key)
        if targets:
            lines.append(f"- {'Blocks' if is_vi() else 'Blocks'}: "+", ".join(_issue_link(k,base) for k in sorted(set(targets))))
        if blocked:
            lines.append(f"- {'Directly blocked by' if is_vi() else 'Directly blocked by'}: "+", ".join(_issue_link(k,base) for k in sorted(set(blocked))))
        if not st.issue.assignee:
            lines.append("- Unassigned")
        life=ri_by.get(key)
        if life and life.propagated_downstream:
            lines.append(f"- {'Propagated impact' if is_vi() else 'Propagated impact'}: "+", ".join(_issue_link(k,base) for k in life.propagated_downstream))
        lines.append("")
    return lines


def _dependency_section(ri,base,limit):
    all_clusters=build_dependency_clusters(ri)
    shown=all_clusters[:limit]
    title=(f"## Active Delivery Dependency Hotspots — Top {len(shown)} of {len(all_clusters)}" if all_clusters else "## Active Delivery Dependency Hotspots")
    lines=[title,""]
    if not shown:
        return lines+[("- Không có active dependency hotspot đáng kể." if is_vi() else "- No material active dependency hotspots."),""]
    for c in shown:
        root=_issue_link(c.root_issue_key,base)
        if is_vi():
            lines.append(f"- **Root {root}** — ảnh hưởng **{len(c.affected_issue_keys)}** downstream issue qua độ sâu **{c.max_depth}**; heuristic pressure **{c.aggregate_pressure}**")
        else:
            lines.append(f"- **Root {root}** — affects **{len(c.affected_issue_keys)}** downstream issue(s) across depth **{c.max_depth}**; heuristic pressure **{c.aggregate_pressure}**")
        if c.direct_downstream:
            lines.append("  - "+("Direct: " if is_vi() else "Direct: ")+", ".join(_issue_link(k,base) for k in c.direct_downstream))
        if c.propagated_downstream:
            lines.append("  - "+("Propagated: " if is_vi() else "Propagated: ")+", ".join(_issue_link(k,base) for k in c.propagated_downstream))
    return lines+[""]



def _dependency_hygiene_section(project_state,base):
    """Render stale/verification relationships separately from active risk.

    These are Jira topology items that need human confirmation. They must not
    be presented as current blockers or root causes until deterministic
    blocking signals confirm them again.
    """
    lines=["## Dependency Hygiene / Needs Verification",""]
    items=[]
    for st in project_state.issues:
        codes={s.code for s in st.signals}
        hygiene_codes=sorted(codes & {"DEPENDENCY_NEEDS_VERIFICATION","STALE_DEPENDENCY_CANDIDATE"})
        if not hygiene_codes:
            continue
        refs=[]
        for d in (st.issue.dependencies or []):
            if d.related_issue_key:
                refs.append(f"{d.relation} {_issue_link(d.related_issue_key,base)}")
        detail=("; ".join(refs) if refs else "không có raw dependency link" if is_vi() else "no raw dependency link")
        items.append((st.issue.key,hygiene_codes,detail))
    if not items:
        return lines+[("- Không có dependency cần verify." if is_vi() else "- No dependencies require verification."),""]
    for key,codes,detail in items[:8]:
        label=", ".join(codes)
        if is_vi():
            lines.append(f"- {_issue_link(key,base)} — **{label}**; raw topology: {detail}")
        else:
            lines.append(f"- {_issue_link(key,base)} — **{label}**; raw topology: {detail}")
    if len(items)>8:
        lines.append((f"- +{len(items)-8} issue khác cần verify trong run log." if is_vi() else f"- +{len(items)-8} additional issue(s) require verification in the run log."))
    lines.append("")
    return lines

def _change_section(delta,base,limit):
    title="## Since Last Run"; lines=[title,""]
    summary=build_change_summary(delta,detail_limit=limit,burst_threshold=20)
    events=[e for e in delta.events if e.category!="ongoing"]
    if summary.mode=="BASELINE": return lines+[("- Đã tạo baseline." if is_vi() else "- Baseline created."),""]
    if not events: return lines+[("- Không có material delivery changes; các risk hiện tại vẫn chưa được giải quyết." if is_vi() else "- No material delivery changes; existing risks remain unresolved."),""]
    grouped={}
    for e in events: grouped.setdefault(e.issue_key or "Project",[]).append(e)
    groups=list(grouped.items())
    if len(events)>20: lines.append((f"- Có **{len(events)}** material changes trên **{len(groups)}** issue; chỉ giữ các thay đổi quan trọng nhất." if is_vi() else f"- **{len(events)}** material changes across **{len(groups)}** issues; only the most important are listed."))
    for key,evs in groups[:limit]:
        labels=[]; added=[]; resolved=[]
        for e in evs:
            if e.code=="SIGNAL_ADDED":
                sig=e.metadata.get("signal")
                if sig and sig not in added: added.append(sig)
            elif e.code=="SIGNAL_RESOLVED":
                sig=e.metadata.get("signal")
                if sig and sig not in resolved: resolved.append(sig)
            else:
                lab=_delta_label(e.code)
                if lab not in labels: labels.append(lab)
        if added: labels.append("new signals: "+", ".join(added))
        if resolved: labels.append("resolved signals: "+", ".join(resolved))
        ref=_issue_link(key,base) if key!="Project" else key
        lines.append(f"- {ref} — "+"; ".join(labels))
    if len(groups)>limit: lines.append((f"- +{len(groups)-limit} issue có thay đổi khác lưu trong run log." if is_vi() else f"- +{len(groups)-limit} additional changed issue(s) retained in the run log."))
    return lines+[""]

def _escalation_section(ri,base):
    title="## Rule-based Escalation Signals" if is_vi() else "## Rule-based Escalation Signals"; lines=[title,""]
    if not ri or not ri.escalation_candidates:return lines+["- Không có ứng viên escalation." if is_vi() else "- No escalation candidates.",""]
    for x in ri.escalation_candidates:
        reasons="; ".join(_translate_reason(r) for r in x.escalation_reasons)
        lines.append(f"- {_issue_link(x.issue_key,base)} — {reasons}")
    return lines+[""]


def _action_section(ai,project_state,hotspots,ri,base):
    title="## PM Actions" if is_vi() else "## Recommended PM Actions"; lines=[title,""]
    # Prefer validated AI actions; deterministic fallback is already leverage-aware.
    actions=list(ai.pm_actions) if ai and ai.pm_actions else []
    if not actions:
        actions=[re.sub(r'^\d+\.\s*','',x) for x in markdown_fallback_actions(project_state,hotspots,ri,base)]
    for i,a in enumerate(actions[:6],1):
        # Link raw issue keys if AI output is plain text.
        a=_link_keys_markdown(a,base)
        lines.append(f"{i}. {a}")
    return lines+[""]


def _observation_section(ai,hotspots,ri,base):
    title="## Key Observations" if is_vi() else "## Important Observations"; lines=[title,""]
    obs=list(ai.observations) if ai and ai.observations else []
    if not obs:
        leverage=build_management_leverage(ri)
        clusters=build_dependency_clusters(ri)
        if clusters and clusters[0].affected_issue_keys:
            c=clusters[0]
            txt=(f"{c.root_issue_key} là active dependency hotspot ảnh hưởng {len(c.affected_issue_keys)} downstream issue." if is_vi() else f"{c.root_issue_key} is an active dependency hotspot affecting {len(c.affected_issue_keys)} downstream issues.")
            obs.append(txt)
        if leverage:
            txt=(f"{leverage[0].issue_key} có rule-based management leverage cao nhất." if is_vi() else f"{leverage[0].issue_key} has the highest rule-based management leverage hint.")
            if txt not in obs:obs.append(txt)
    for o in obs[:5]:lines.append("- "+_link_keys_markdown(o,base))
    return lines+[""]


def _hotspot_section(hotspots,base):
    title="## Deterministic Hotspots"; lines=[title,""]
    if not hotspots or not hotspots.items:return lines+["- Không có hotspot.",""]
    lines.append("| Issue | Hotspot Priority | Pressure | Reasons |")
    lines.append("|---|---:|---:|---|")
    for h in hotspots.items:
        reasons=", ".join(_translate_reason(r) for r in h.reasons)
        lines.append(f"| {_issue_link(h.issue_key,base)} | {risk_label(h.level)} | {h.score} | {reasons} |")
    return lines+[""]


def _evidence_section(project_state,base):
    url=project_url(project_state.project_key,base); label=source_name().title()
    if is_vi():return ["## Nguồn dữ liệu","",f"- {label} project: {url}","- Toàn bộ issue, raw delta và lifecycle kỹ thuật vẫn được giữ trong run log.",""]
    return ["## Evidence","",f"- {label} project: {url}","- Full technical evidence, raw delta and lifecycle details are retained in the run log.",""]


def _link_keys_markdown(text,base):
    if not text:return ""
    # Avoid nesting links by only replacing keys not immediately preceded by '['.
    return re.sub(r'(?<!\[)\b([A-Z][A-Z0-9_]*-\d+)\b',lambda m:_issue_link(m.group(1),base),str(text))


def _translate_reason(text: str) -> str:
    if not is_vi():
        return text
    mapping = {
        "overdue": "quá hạn",
        "blocking downstream work": "đang block downstream tasks",
        "blocked": "đang bị chặn",
        "persistent blocker": "blocker kéo dài qua nhiều snapshot",
        "near due": "sắp đến hạn",
        "stuck in active work": "kẹt ở trạng thái đang xử lý",
        "stale active work": "active tasks thiếu cập nhật",
        "workflow inconsistency": "không nhất quán workflow",
        "dependency needs verification": "dependency cần xác minh",
        "critical delivery pressure": "critical delivery pressure",
    }
    low = text.lower().strip()
    if low in mapping:
        return mapping[low]
    if low.startswith("overdue for >="):
        return text.replace("overdue for >=", "quá hạn >=")
    if low.startswith("affects "):
        return text.replace("affects", "ảnh hưởng", 1).replace("direct", "trực tiếp").replace("propagated", "lan truyền").replace("downstream issues", "issue downstream")
    return text


def _delta_label(code: str) -> str:
    if not is_vi():
        return code
    return {
        "ISSUE_ADDED": "issue mới được thêm",
        "ISSUE_REMOVED": "issue đã bị loại khỏi dự án",
        "ISSUE_REOPENED": "issue được mở lại",
        "STATUS_CHANGED": "trạng thái cuối cùng đã thay đổi",
        "ASSIGNEE_CHANGED": "người phụ trách cuối cùng đã thay đổi",
        "DUE_DATE_CHANGED": "ngày đến hạn cuối cùng đã thay đổi",
        "DEPENDENCY_ADDED": "có dependency mới",
        "DEPENDENCY_REMOVED": "dependency đã được gỡ",
        "SIGNAL_ADDED": "xuất hiện tín hiệu rủi ro mới",
        "SIGNAL_RESOLVED": "một tín hiệu rủi ro đã được giải quyết",
        "PERSISTENT_BLOCKER": "blocker vẫn tồn tại qua nhiều snapshot",
        "NO_PROGRESS": "không có tiến triển đáng kể",
    }.get(code, code)
