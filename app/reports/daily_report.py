from html import escape

from app.ai.models import ProjectAIAnalysis
from app.i18n import is_vi
from app.intelligence.hotspots import ProjectHotspots
from app.source_urls import project_url, source_name
from app.reports.deterministic_brief import build_fallback_actions, build_fallback_assessment, build_fallback_key_risks, build_fallback_observations, risk_relevant_delta_lines
from app.reports.sections.ai_assessment import build_ai_assessment_section
from app.reports.sections.delta import build_delta_section
from app.reports.sections.overview import build_header_section
from app.reports.sections.risk_intelligence import build_risk_intelligence_section


def build_daily_report(project_state,metrics,project_risk,intelligence,delta,jira_base_url:str,ai_analysis:ProjectAIAnalysis|None=None,hotspots:ProjectHotspots|None=None,risk_intelligence=None,*,report_filename:str|None=None,max_risks:int=5,max_actions:int=4,max_observations:int=2,change_detail_limit:int=5,burst_threshold:int=20)->str:
    lines=[]; lines.extend(build_header_section(project_state,report_filename=report_filename))
    if ai_analysis is not None:
        section=build_ai_assessment_section(ai_analysis,jira_base_url,max_risks=max_risks,max_actions=max_actions,max_observations=max_observations)
        if section: lines.extend(section.splitlines())
        lines.append("")
    else:
        lines.extend(build_fallback_assessment(project_state,metrics,intelligence,hotspots,risk_intelligence))
        lines.extend(build_fallback_key_risks(project_state,hotspots,risk_intelligence,limit=max_risks))
        lines.extend(build_fallback_actions(project_state,hotspots,risk_intelligence,limit=max_actions))
        lines.extend(build_fallback_observations(hotspots,risk_intelligence))
    if ai_analysis is None:
        lines.extend(["📈 <b>Thay đổi từ lần chạy trước</b>" if is_vi() else "📈 <b>Since last run</b>",*risk_relevant_delta_lines(delta,hotspots,limit=change_detail_limit),""])
    else:
        lines.extend(build_delta_section(delta,hotspots,include_ongoing=False,detail_limit=change_detail_limit,burst_threshold=burst_threshold))
    if risk_intelligence is not None: lines.extend(build_risk_intelligence_section(risk_intelligence))
    completion=round(metrics.done_issues/metrics.total_issues*100) if metrics.total_issues else 0
    if is_vi():
        lines.extend(["📊 <b>Tổng quan dự án</b>",f"• {metrics.total_issues} issue · {metrics.active_issues} đang hoạt động · {metrics.done_issues} hoàn thành · {completion}% hoàn tất",f"• {metrics.overdue_issues} quá hạn · {metrics.near_due_issues} sắp đến hạn · {metrics.blocked_issues} bị chặn · {metrics.blocking_issues} blocker đang hoạt động",""])
    else:
        lines.extend(["📊 <b>Project Snapshot</b>",f"• {metrics.total_issues} issues · {metrics.active_issues} active · {metrics.done_issues} done · {completion}% complete",f"• {metrics.overdue_issues} overdue · {metrics.near_due_issues} near due · {metrics.blocked_issues} blocked · {metrics.blocking_issues} active blockers",""])
    return "\n".join(lines)


def build_minimal_daily_report(project_state,metrics,intelligence,risk_intelligence,hotspots,jira_base_url:str)->str:
    # Kept for compatibility; normal run uses progressive compression instead.
    return build_fallback_assessment(project_state,metrics,intelligence,hotspots,risk_intelligence)[0]


def build_source_section(project_state)->list[str]:
    if not project_state.issues:return []
    url=project_url(project_state.project_key)
    label="Nguồn bằng chứng" if is_vi() else "Evidence source"
    return [f'🔎 <b>{label}:</b> <a href="{escape(url)}">{source_name().title()}</a>']
