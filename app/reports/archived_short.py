"""Read the original archived daily brief without invoking AI or publishers."""
from html import unescape
from pathlib import Path
import os
import re


def _markdown(message: str) -> str:
    message = re.sub(r'<a href="(https?://[^"<>]+)">([^<]*)</a>', r'[\2](\1)', message)
    message = re.sub(r'<(?:b|strong)>(.*?)</(?:b|strong)>', r'**\1**', message)
    message = re.sub(r'<[^>]*>', '', message)
    lines = []
    for line in unescape(message).splitlines():
        if re.match(r'^[🧠🔥🎯💡📈🧭📊]\s+\*\*', line):
            line = '### ' + line.replace('**', '')
        lines.append(line)
    return "\n".join(lines).strip()


def archived_short(report: Path, identifier: str, text: str) -> str:
    companion = report.with_suffix('.short.html')
    if companion.is_file() and companion.resolve().parent == report.resolve().parent:
        return _markdown(companion.read_text(encoding='utf-8'))
    root = Path(os.getenv('RUN_LOG_DIRECTORY', 'data/logs'))
    if not root.is_absolute():
        root = Path(__file__).resolve().parents[2] / root
    root = root.resolve()
    project_dir = (root / identifier).resolve()
    if project_dir.parent == root:
        for log in sorted(project_dir.glob('*.md'), reverse=True):
            if log.resolve().parent != project_dir:
                continue
            content = log.read_text(encoding='utf-8')
            message = re.search(r'^## Telegram Daily Message\s*\n\s*```html\n(.*?)\n```', content, re.M | re.S)
            if message and report.name in message.group(1):
                return _markdown(message.group(1))
    # Historical imports may lack a companion or a matching run log. Preserve
    # existing evidence rather than fabricate an original Telegram message.
    parts = []
    headings = [
        ('Đánh giá tổng quan|Executive Assessment', '🧠 Project Assessment'),
        ('Priority Risks', '🔥 Key Risks'), ('PM Actions', '🎯 PM Actions'),
        ('Key Observations', '💡 Observations'), ('Since Last Run', '📈 Since Last Run'),
        ('Rule-based Escalation Signals', '🧭 Risk Lifecycle'),
        ('Tổng quan dự án|Project Snapshot', '📊 Tổng quan dự án'),
    ]
    for pattern, title in headings:
        section = re.search(r'^## (?:' + pattern + r')\s*\n(.*?)(?=^## |\Z)', text, re.M | re.S)
        if section:
            parts.append('### ' + title + '\n' + section.group(1).strip())
    return "\n\n".join(parts)
