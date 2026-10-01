from app.i18n import is_vi, trend_label
from app.intelligence.risk_intelligence import RiskIntelligence
from app.reports.helpers import issue_ref


def _impact_phrase(item) -> str | None:
    direct=len(item.direct_downstream); propagated=len(item.propagated_downstream)
    if not (direct or propagated): return None
    if is_vi():
        if propagated: return f"ảnh hưởng {direct} issue trực tiếp + {propagated} issue lan truyền"
        return f"ảnh hưởng {direct} issue downstream trực tiếp"
    if propagated: return f"affects {direct} direct + {propagated} propagated downstream issue(s)"
    return f"affects {direct} direct downstream issue(s)"


def _reason_vi(reason: str) -> str:
    r=reason.lower()
    if "critical delivery pressure" in r: return "critical delivery pressure"
    if "overdue for >=" in r: return r.replace("overdue for >=", "quá hạn >=")
    if "propagated" in r: return reason
    return reason


def build_risk_intelligence_section(risk_intelligence: RiskIntelligence, *, escalation_limit: int = 3) -> list[str]:
    lines=["🧭 <b>Risk Lifecycle</b>" if is_vi() else "🧭 <b>Risk Lifecycle</b>"]
    if risk_intelligence.previous_project_score is None:
        txt=f"• Baseline Risk Pressure: {risk_intelligence.project_score}" if is_vi() else f"• Baseline risk pressure: {risk_intelligence.project_score}"
        return lines+[txt,""]
    icon={"UP":"🔺","DOWN":"🔻","STABLE":"➡️"}.get(risk_intelligence.project_trend,"•")
    label="Risk Pressure"
    lines.append(f"• {icon} {label}: {risk_intelligence.previous_project_score} → {risk_intelligence.project_score} · {trend_label(risk_intelligence.project_trend)}")
    for item in risk_intelligence.escalation_candidates[:escalation_limit]:
        reasons=[r for r in item.escalation_reasons if not r.startswith("affects ")]
        if is_vi(): reasons=[_reason_vi(r) for r in reasons]
        impact=_impact_phrase(item)
        if impact: reasons.append(impact)
        suffix="; ".join(reasons)
        title="cần escalation" if is_vi() else "escalation candidate"
        lines.append(f"• 🚨 {issue_ref(item.issue_key)} {title}" + (f" — {suffix}" if suffix else ""))
    lines.append("")
    return lines
