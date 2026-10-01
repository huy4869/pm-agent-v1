from __future__ import annotations

import html
import os
import time

from app.domain.project_state import build_project_state
from app.metrics.project_metrics import calculate_project_metrics
from app.resource.ai_reasoner import analyze_allocation
from app.resource.engine import describe_member
from app.resource.formatter import format_ai_allocation
from app.sources import build_collector
from app.telegram.client import TelegramClient

RA_HINTS = (
    "ai rảnh", "ai đang rảnh", "ai làm được", "giao ai", "allocate",
    "allocation", "resource", "nhận được", "phù hợp", "available",
)


def _state():
    collector, _ = build_collector()
    state = build_project_state(collector)
    state.metrics = calculate_project_metrics(state)
    return state


def answer(text: str) -> str:
    clean = text.strip()
    if clean.lower() in {"/start", "/help", "help"}:
        return (
            "🤖 <b>PM Agent</b>\nBạn có thể hỏi tự nhiên:\n"
            "• Có task backend 3 ngày bắt đầu ngày mai, ai làm được?\n"
            "• Ai đang rảnh nhất?\n• tran huy đang làm gì?\n"
            "• /ra backend 3 ngày"
        )
    state = _state()
    member = describe_member(state, clean)
    if member and any(hint in clean.lower() for hint in ("đang làm", "workload", "task nào", "làm gì")):
        return member
    if clean.lower().startswith("/ra") or any(hint in clean.lower() for hint in RA_HINTS):
        result, provider = analyze_allocation(state, clean)
        return format_ai_allocation(result, provider)
    return (
        "Mình chưa chắc bạn đang hỏi loại phân tích nào. Hiện bot hỗ trợ "
        "<b>Resource Allocation</b> và workload member. Ví dụ: "
        "<i>Có task backend 3 ngày bắt đầu ngày mai, ai làm được?</i>"
    )


def run_bot() -> None:
    client = TelegramClient()
    offset = None
    allowed = os.getenv("TELEGRAM_CHAT_ID", "").strip()
    print("PM Agent Telegram bot listening... Ctrl+C to stop")
    while True:
        try:
            for update in client.get_updates(offset=offset, timeout=30):
                offset = update["update_id"] + 1
                message = update.get("message") or {}
                text = message.get("text")
                chat_id = str((message.get("chat") or {}).get("id", ""))
                if not text or not chat_id:
                    continue
                if allowed and chat_id != allowed:
                    continue
                try:
                    reply = answer(text)
                except Exception as exc:
                    detail = html.escape(f"{type(exc).__name__}: {exc}")
                    reply = f"⚠️ Không thể phân tích lúc này: {detail}"
                client.send_message(reply, chat_id=chat_id)
        except KeyboardInterrupt:
            break
        except Exception as exc:
            print(f"Telegram polling error: {exc}")
            time.sleep(5)
