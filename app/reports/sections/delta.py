from html import escape
from collections import OrderedDict
from app.i18n import is_vi
from app.intelligence.change_summary import build_change_summary
from app.intelligence.hotspots import ProjectHotspots
from app.memory.delta import ProjectDelta
from app.reports.helpers import issue_ref

def _group_events(events):
    groups=OrderedDict()
    for e in events: groups.setdefault(e.issue_key or '__PROJECT__',[]).append(e)
    return list(groups.values())

def build_delta_section(delta: ProjectDelta, hotspots: ProjectHotspots | None = None, *, include_ongoing: bool = True, detail_limit: int = 5, burst_threshold: int = 20) -> list[str]:
    lines=['📈 <b>Since Last Run</b>']; summary=build_change_summary(delta,detail_limit=detail_limit,burst_threshold=burst_threshold)
    if summary.mode=='BASELINE': return lines+['• Đã tạo baseline — chưa có snapshot trước đó' if is_vi() else '• Baseline created — no previous snapshot','']
    events=[]
    for e in delta.events:
        if e.code=='NO_PROGRESS' and hotspots is not None and not hotspots.is_significant(e.issue_key): continue
        if not include_ongoing and e.category=='ongoing': continue
        events.append(e)
    groups=_group_events(events)
    if not groups: return lines+['• Không có material delivery changes; các risk hiện tại vẫn chưa được giải quyết' if is_vi() else '• No material delivery changes; existing risks remain unresolved','']
    if summary.mode in {'BURST','SUMMARIZED'} or len(events)>burst_threshold:
        lines.append(f'• Có {summary.material_events} material changes; chỉ hiển thị các thay đổi ảnh hưởng risk nhất' if is_vi() else f'• {summary.material_events} material changes detected; showing only the most risk-relevant changes')
    for g in groups[:detail_limit]: lines.append(_format_group(g))
    if len(groups)>detail_limit: lines.append(f'• +{len(groups)-detail_limit} issue có thay đổi khác trong file báo cáo' if is_vi() else f'• +{len(groups)-detail_limit} additional changed issue(s) in detailed report')
    return lines+['']

def _format_group(group):
    key=issue_ref(group[0].issue_key) if group[0].issue_key else 'Project'; parts=[]; added=[]; resolved=[]
    for e in group:
        if e.code=='SIGNAL_ADDED':
            sig=e.metadata.get('signal'); added += [sig] if sig and sig not in added else []
        elif e.code=='SIGNAL_RESOLVED':
            sig=e.metadata.get('signal'); resolved += [sig] if sig and sig not in resolved else []
        else:
            label=_event_phrase(e)
            if label and label not in parts: parts.append(label)
    if added: parts.append('new signals: '+', '.join(added))
    if resolved: parts.append('resolved signals: '+', '.join(resolved))
    prefix='⚠️' if any(e.severity=='warning' for e in group) else '•'
    return f"{prefix} {key} — "+'; '.join(parts or ['final state changed'])

def _event_phrase(e):
    if is_vi():
        return {'ISSUE_ADDED':'issue mới được thêm','ISSUE_REMOVED':'issue đã bị loại khỏi project','PERSISTENT_BLOCKER':'vẫn là persistent blocker','NO_PROGRESS':'không có progress gần đây','DUE_DATE_CHANGED':'due date đã thay đổi','ISSUE_REOPENED':'reopened','DEPENDENCY_ADDED':'dependency mới','DEPENDENCY_REMOVED':'dependency đã được gỡ','STATUS_CHANGED':'status đã thay đổi','ASSIGNEE_CHANGED':'owner đã thay đổi'}.get(e.code,escape(e.message))
    return escape(e.message)
