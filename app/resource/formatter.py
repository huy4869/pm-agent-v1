from __future__ import annotations

import html

ICONS = {"RECOMMENDED": "🟢", "POSSIBLE": "🟡", "NOT_RECOMMENDED": "🔴", "NEEDS_VERIFICATION": "🔎"}
LABELS = {"RECOMMENDED": "Recommended", "POSSIBLE": "Possible", "NOT_RECOMMENDED": "Not recommended", "NEEDS_VERIFICATION": "Needs verification"}


def format_ai_allocation(result: dict, provider: str | None = None) -> str:
    escape = lambda value: html.escape(str(value or ""))
    lines = ["🧠 <b>AI Resource Allocation</b>"]
    if result.get("understood_request"):
        lines.append(f"<b>Yêu cầu:</b> {escape(result['understood_request'])}")
    if result.get("assessment"):
        lines += ["", escape(result["assessment"])]
    candidates = result.get("candidates") or []
    if candidates:
        lines += ["", "👥 <b>Đánh giá resource</b>"]
        for candidate in candidates[:6]:
            verdict = candidate.get("verdict", "NEEDS_VERIFICATION")
            lines.append(f"{ICONS.get(verdict, '•')} <b>{escape(candidate.get('name'))}</b> — {LABELS.get(verdict, escape(verdict))}")
            lines.extend(f"• {escape(reason)}" for reason in (candidate.get("reasoning") or [])[:4])
            lines.extend(f"• ⚠️ {escape(risk)}" for risk in (candidate.get("risks") or [])[:2])
    lines += ["", "🎯 <b>Recommendation</b>", escape(result.get("recommendation") or "Chưa đủ dữ liệu để đưa ra recommendation.")]
    if result.get("alternatives"):
        lines += ["", "🔄 <b>Phương án khác</b>"] + [f"• {escape(item)}" for item in result["alternatives"][:4]]
    if result.get("missing_information"):
        lines += ["", "❓ <b>Cần xác minh thêm</b>"] + [f"• {escape(item)}" for item in result["missing_information"][:4]]
    lines += ["", f"<b>Confidence:</b> {escape(result.get('confidence', 'MEDIUM'))}"]
    if provider:
        lines.append(f"<i>Reasoned by {escape(provider)} · không dùng allocation score</i>")
    return "\n".join(lines)
