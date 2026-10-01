from __future__ import annotations

from html import escape

from app.i18n import health_label, is_vi, risk_label
from app.intelligence.change_summary import build_change_summary
from app.intelligence.dependency_clusters import build_dependency_clusters
from app.intelligence.management_leverage import build_management_leverage
from app.reports.helpers import issue_ref, blocking_targets, signal_codes


def build_fallback_assessment(project_state, metrics, intelligence, hotspots, risk_intelligence) -> list[str]:
    health=intelligence.health
    icon={"HEALTHY":"🟢","WATCH":"🟡","AT_RISK":"🟠","CRITICAL":"🔴"}.get(health,"⚪️")
    clusters=build_dependency_clusters(risk_intelligence)
    critical=[h.issue_key for h in (hotspots.items if hotspots else []) if h.level=="CRITICAL"][:3]
    if is_vi():
        parts=[]
        if critical: parts.append("áp lực delivery tập trung ở "+", ".join(issue_ref(k) for k in critical))
        if clusters and len(clusters[0].affected_issue_keys)>=2:
            c=clusters[0]; chain=[c.root_issue_key]+_walk_chain(c.root_issue_key,risk_intelligence)
            if len(chain)>1: parts.append("chuỗi dependency "+" → ".join(issue_ref(k) for k in chain)+" tạo rủi ro downstream")
        if not parts: parts.append(_fallback_fact(metrics))
        summary=f"Dự án {escape(project_state.project_key)} đang ở mức <b>{health_label(health)}</b>: "+"; đồng thời ".join(parts)+"."
        return ["🧠 <b>Đánh giá dự án</b>","",f"{icon} <b>{health_label(health)}</b>",summary,""]
    parts=[]
    if critical: parts.append("delivery pressure is concentrated around "+", ".join(issue_ref(k) for k in critical))
    if clusters and len(clusters[0].affected_issue_keys)>=2:
        c=clusters[0]; chain=[c.root_issue_key]+_walk_chain(c.root_issue_key,risk_intelligence)
        if len(chain)>1: parts.append("the dependency chain "+" → ".join(issue_ref(k) for k in chain)+" creates downstream exposure")
    if not parts: parts.append(_fallback_fact(metrics))
    return ["🧠 <b>Project Assessment</b>","",f"{icon} <b>{health}</b>",f"Project {escape(project_state.project_key)} is <b>{health}</b>: "+"; while ".join(parts)+".",""]


def build_fallback_key_risks(project_state, hotspots, risk_intelligence, *, limit:int=4)->list[str]:
    if not hotspots or not hotspots.items: return []
    states={s.issue.key:s for s in project_state.issues}; ri={i.issue_key:i for i in risk_intelligence.items} if risk_intelligence else {}
    lines=["🔥 <b>Rủi ro trọng yếu</b>" if is_vi() else "🔥 <b>Key Risks</b>",""]
    icons={"CRITICAL":"🔴","HIGH":"🟠","MEDIUM":"🟡","LOW":"🟢"}
    for h in hotspots.items[:limit]:
        state=states.get(h.issue_key)
        if not state: continue
        lines.append(f"{icons.get(h.level,'⚪️')} {issue_ref(h.issue_key)} — <b>{risk_label(h.level)}</b>")
        for fact in _risk_facts(state,h,ri.get(h.issue_key))[:3]: lines.append(f"• {fact}")
        lines.append("")
    return lines


def build_fallback_actions(project_state, hotspots, risk_intelligence, *, limit:int=4)->list[str]:
    states={s.issue.key:s for s in project_state.issues}; actions=[]
    leverage=build_management_leverage(risk_intelligence)
    clusters={c.root_issue_key:c for c in build_dependency_clusters(risk_intelligence)}
    for lev in leverage:
        if len(actions)>=limit: break
        state=states.get(lev.issue_key)
        if not state: continue
        cluster=clusters.get(lev.issue_key)
        if cluster and cluster.affected_issue_keys:
            chain=[lev.issue_key]+_walk_chain(lev.issue_key,risk_intelligence)
            if is_vi():
                owner=(f"Gán owner cho {issue_ref(lev.issue_key)} và " if not state.issue.assignee else f"Theo dõi với {escape(state.issue.assignee)} về {issue_ref(lev.issue_key)} và ")
                actions.append(owner+"chốt kế hoạch xử lý chuỗi "+" → ".join(issue_ref(k) for k in chain)+".")
            else:
                owner=(f"Assign an owner to {issue_ref(lev.issue_key)} and " if not state.issue.assignee else f"Follow up with {escape(state.issue.assignee)} on {issue_ref(lev.issue_key)} and ")
                actions.append(owner+"confirm the recovery plan for chain "+" → ".join(issue_ref(k) for k in chain)+".")
            continue
        if not state.issue.assignee and "BLOCKING_OTHERS" in signal_codes(state):
            actions.append((f"Gán owner cho {issue_ref(lev.issue_key)} và xác nhận ETA unblock." if is_vi() else f"Assign an owner to {issue_ref(lev.issue_key)} and confirm an unblock ETA."))
        elif state.issue.assignee and ("OVERDUE" in signal_codes(state) or "BLOCKING_OTHERS" in signal_codes(state)):
            actions.append((f"Theo dõi với {escape(state.issue.assignee)} về {issue_ref(lev.issue_key)} và xác nhận ETA/kế hoạch phục hồi." if is_vi() else f"Follow up with {escape(state.issue.assignee)} on {issue_ref(lev.issue_key)} and confirm the ETA/recovery plan."))
    # dedupe
    dedup=[]
    for a in actions:
        if a not in dedup: dedup.append(a)
    title="🎯 <b>Hành động PM đề xuất</b>" if is_vi() else "🎯 <b>Recommended PM Actions</b>"
    return [title,*[f"{i}. {a}" for i,a in enumerate(dedup[:limit],1)],""] if dedup else []


def build_fallback_observations(hotspots,risk_intelligence)->list[str]:
    obs=[]; clusters=build_dependency_clusters(risk_intelligence); leverage=build_management_leverage(risk_intelligence)
    if clusters:
        c=clusters[0]
        if len(c.affected_issue_keys)>=2:
            obs.append((f"{issue_ref(c.root_issue_key)} là active root dependency ảnh hưởng {len(c.affected_issue_keys)} issue downstream qua độ sâu {c.max_depth}." if is_vi() else f"{issue_ref(c.root_issue_key)} is an active root dependency risk affecting {len(c.affected_issue_keys)} downstream issue(s) across depth {c.max_depth}."))
    if leverage and hotspots and hotspots.items and leverage[0].issue_key != hotspots.items[0].issue_key:
        obs.append((f"{issue_ref(leverage[0].issue_key)} có management leverage cao hơn risk score riêng lẻ vì xử lý root này có thể giải phóng nhiều downstream issue." if is_vi() else f"{issue_ref(leverage[0].issue_key)} has higher management leverage than its individual risk score suggests because resolving the root can release multiple downstream issues."))
    title="💡 <b>Nhận định</b>" if is_vi() else "💡 <b>Observations</b>"
    return [title,*[f"• {o}" for o in obs[:2]],""] if obs else []


def risk_relevant_delta_lines(delta,hotspots,*,limit:int=4)->list[str]:
    summary=build_change_summary(delta,detail_limit=max(limit,5),burst_threshold=20)
    if summary.mode=="BASELINE": return ["• Đã tạo mốc ban đầu — chưa có snapshot trước" if is_vi() else "• Baseline created — no previous snapshot"]
    significant=hotspots.significant_issue_keys if hotspots else set(); risk_codes={"SIGNAL_ADDED","ISSUE_REOPENED","DEPENDENCY_ADDED","DEPENDENCY_REMOVED","DUE_DATE_CHANGED"}
    events=[e for e in summary.top_events if e.code in risk_codes or (e.issue_key in significant and e.severity=="warning")]
    if not events: return ["• Không có thay đổi rủi ro mới đáng kể; các rủi ro hiện tại tiếp tục được theo dõi" if is_vi() else "• No new material risk changes; existing risks remain under lifecycle tracking"]
    lines=[]
    for e in events[:limit]:
        prefix=issue_ref(e.issue_key) if e.issue_key else "Project"
        if is_vi(): lines.append(f"• {prefix} — có thay đổi trạng thái cuối cùng ảnh hưởng delivery")
        else: lines.append(f"• {prefix} — {escape(e.message)}")
    return lines


def markdown_fallback_actions(project_state,hotspots,risk_intelligence,base:str)->list[str]:
    html_lines=build_fallback_actions(project_state,hotspots,risk_intelligence)
    return [_html_issue_refs_to_markdown(line,base) for line in html_lines[1:-1]]


def _risk_facts(state,hotspot,ri_item)->list[str]:
    codes=signal_codes(state); facts=[]
    if "OVERDUE" in codes and state.metrics.days_to_due is not None:
        d=abs(state.metrics.days_to_due); facts.append(f"Quá hạn <b>{d} ngày</b>" if is_vi() else f"Overdue by <b>{d} day(s)</b>")
    targets=blocking_targets(state.issue)
    if targets: facts.append(("Chặn " if is_vi() else "Blocks ")+", ".join(issue_ref(k) for k in targets))
    blocked_by=sorted({d.related_issue_key for d in (state.issue.dependencies or []) if "blocked by" in d.relation.lower()})
    if blocked_by: facts.append(("Bị chặn trực tiếp bởi " if is_vi() else "Directly blocked by ")+", ".join(issue_ref(k) for k in blocked_by))
    if "PERSISTENT_BLOCKER" in hotspot.delta_codes: facts.append("Vẫn là blocker qua nhiều snapshot" if is_vi() else "Persistent blocker across snapshots")
    if ri_item and ri_item.propagated_downstream: facts.append((f"Ảnh hưởng root: {len(ri_item.direct_downstream)} trực tiếp + {len(ri_item.propagated_downstream)} lan truyền" if is_vi() else f"Root impact: {len(ri_item.direct_downstream)} direct + {len(ri_item.propagated_downstream)} propagated issue(s)"))
    return facts or [escape(r) for r in hotspot.reasons[:2]]


def _walk_chain(root,risk_intelligence,max_depth=5):
    if not risk_intelligence:return []
    by={i.issue_key:i for i in risk_intelligence.items}; out=[]; seen={root}; cur=root
    for _ in range(max_depth):
        item=by.get(cur)
        if not item or not item.direct_downstream: break
        nxt=item.direct_downstream[0]
        if nxt in seen: break
        out.append(nxt); seen.add(nxt); cur=nxt
    return out


def _fallback_fact(metrics):
    if is_vi():
        facts=[]
        if metrics.overdue_issues:facts.append(f"{metrics.overdue_issues} quá hạn")
        if metrics.blocked_issues:facts.append(f"{metrics.blocked_issues} bị chặn")
        if metrics.blocking_issues:facts.append(f"{metrics.blocking_issues} blocker đang hoạt động")
        return ", ".join(facts) or "không phát hiện áp lực delivery đáng kể"
    facts=[]
    if metrics.overdue_issues:facts.append(f"{metrics.overdue_issues} overdue")
    if metrics.blocked_issues:facts.append(f"{metrics.blocked_issues} blocked")
    if metrics.blocking_issues:facts.append(f"{metrics.blocking_issues} active blockers")
    return ", ".join(facts) or "no material delivery pressure detected"


def _html_issue_refs_to_markdown(text,base):
    import re
    from app.source_urls import issue_url
    return re.sub(
        r'<a href="[^"]+">([A-Z][A-Z0-9_]*-\d+)</a>',
        lambda m: f"[{m.group(1)}]({issue_url(m.group(1), base)})",
        text,
    )
