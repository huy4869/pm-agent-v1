import html
import re

from app.ai.models import ProjectAIAnalysis, RiskEvidence
from app.i18n import health_label, is_vi, risk_label
from app.reports.helpers import issue_ref
from app.source_urls import issue_url

ISSUE_KEY_PATTERN = re.compile(r"\b[A-Z][A-Z0-9_]*-\d+\b")


def _link_issue_keys(text: str, jira_base_url: str) -> str:
    if not text: return ""
    escaped=html.escape(str(text))
    def repl(m):
        k=m.group(0); url=issue_url(k, jira_base_url)
        return f'<a href="{html.escape(url)}">{html.escape(k)}</a>'
    return ISSUE_KEY_PATTERN.sub(repl,escaped)


def _health_icon(h): return {"HEALTHY":"🟢","WATCH":"🟡","AT_RISK":"🟠","CRITICAL":"🔴"}.get(h,"⚪️")
def _risk_icon(h): return {"LOW":"🟢","MEDIUM":"🟡","HIGH":"🟠","CRITICAL":"🔴"}.get(h,"⚪️")
def _normalize_unassigned(v): return v is None or v.strip().lower() in {"","none","null","unassigned"}
def _normalize_overdue_value(v):
    if not v: return None
    r=v.strip()
    for suffix in (" overdue"," late"):
        if r.lower().endswith(suffix): r=r[:-len(suffix)].strip(); break
    return r or None


def _render_evidence(e: RiskEvidence) -> str | None:
    kind=(e.type or "").upper(); key=e.issue_key; value=e.value; related=e.related_issue_keys
    if not key: return None
    if is_vi():
        if kind=="STATUS" and value: return f"{issue_ref(key)} trạng thái: <b>{html.escape(value)}</b>"
        if kind=="ASSIGNEE": return f"{issue_ref(key)} unassigned" if _normalize_unassigned(value) else f"{issue_ref(key)} owner: <b>{html.escape(value or '')}</b>"
        if kind=="OVERDUE":
            d=_normalize_overdue_value(value)
            if d:
                d=re.sub(r"\s*days?\b", " ngày", d, flags=re.IGNORECASE).strip()
                return f"{issue_ref(key)} quá hạn <b>{html.escape(d)}</b>"
            return f"{issue_ref(key)} đang quá hạn"
        if kind=="NEAR_DUE": return f"{issue_ref(key)} sắp đến hạn"
        if kind=="BLOCKS" and related: return f"{issue_ref(key)} blocks {', '.join(issue_ref(x) for x in related)}"
        if kind=="BLOCKED_BY" and related: return f"{issue_ref(key)} directly blocked by {', '.join(issue_ref(x) for x in related)}"
        if kind=="PERSISTENT_BLOCKER": return f"{issue_ref(key)} vẫn là blocker qua nhiều snapshot"
        if kind=="STALE": return f"{issue_ref(key)} không có cập nhật gần đây"
        if kind=="STUCK": return f"{issue_ref(key)} ở cùng trạng thái hoạt động quá lâu"
        if kind=="DEPENDENCY_VERIFICATION": return f"{issue_ref(key)} có dependency cần xác minh"
    else:
        if kind=="STATUS" and value: return f"{issue_ref(key)} status: <b>{html.escape(value)}</b>"
        if kind=="ASSIGNEE": return f"{issue_ref(key)} is unassigned" if _normalize_unassigned(value) else f"{issue_ref(key)} assigned to <b>{html.escape(value or '')}</b>"
        if kind=="OVERDUE":
            d=_normalize_overdue_value(value); return f"{issue_ref(key)} overdue by <b>{html.escape(d)}</b>" if d else f"{issue_ref(key)} is overdue"
        if kind=="BLOCKS" and related: return f"{issue_ref(key)} blocks {', '.join(issue_ref(x) for x in related)}"
        if kind=="BLOCKED_BY" and related: return f"{issue_ref(key)} is directly blocked by {', '.join(issue_ref(x) for x in related)}"
        if kind=="PERSISTENT_BLOCKER": return f"{issue_ref(key)} remains a blocker across snapshots"
    return None


def _dedupe_observations(a):
    seen=set(); out=[]
    for o in a.observations:
        n=" ".join(o.lower().split())
        if n in seen: continue
        if any(x in n for x in ("issues are currently overdue","issues are overdue","issues are currently unassigned")): continue
        seen.add(n); out.append(o)
    return out


def build_ai_assessment_section(analysis: ProjectAIAnalysis, jira_base_url: str, *, max_risks: int=3, max_actions: int=3, max_observations: int=1) -> str:
    lines=["🧠 <b>AI Project Assessment</b>" if is_vi() else "🧠 <b>AI Project Assessment</b>",""]
    lines.append(f"{_health_icon(analysis.health)} <b>{html.escape(health_label(analysis.health))}</b>")
    if analysis.summary: lines.append(_link_issue_keys(analysis.summary,jira_base_url))
    risks=analysis.risks[:max_risks]
    if risks:
        lines.extend(["", "🔥 <b>Key Risks</b>"])
        for risk in risks:
            lines.extend(["",f"{_risk_icon(risk.level)} {issue_ref(risk.issue_key)} — <b>{html.escape(risk_label(risk.level))}</b>"])
            allowed={"OVERDUE","BLOCKS","BLOCKED_BY","PERSISTENT_BLOCKER","STALE","STUCK","DEPENDENCY_VERIFICATION"}
            rendered=[]
            for e in risk.evidence:
                if e.type.upper() not in allowed: continue
                r=_render_evidence(e)
                if r and r not in rendered: rendered.append(r)
            for r in rendered[:3]: lines.append(f"• {r}")
        if len(analysis.risks)>len(risks):
            n=len(analysis.risks)-len(risks)
            lines.append(f"• +{n} rủi ro khác trong file báo cáo" if is_vi() else f"• +{n} additional risk(s) in detailed report")
    actions=analysis.pm_actions[:max_actions]
    if actions:
        lines.extend(["", "🎯 <b>PM Actions</b>" if is_vi() else "🎯 <b>Recommended PM Actions</b>"])
        for i,a in enumerate(actions,1): lines.append(f"{i}. {_link_issue_keys(a,jira_base_url)}")
    obs=_dedupe_observations(analysis)[:max_observations]
    if obs:
        lines.extend(["", "💡 <b>AI Observations</b>"])
        for o in obs: lines.append("• "+_link_issue_keys(o,jira_base_url))
    return "\n".join(lines)
