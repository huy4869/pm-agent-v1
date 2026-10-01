from __future__ import annotations

import os
from pathlib import Path

import requests
from dotenv import load_dotenv
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

load_dotenv()


class TelegramClient:
    def __init__(self) -> None:
        token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID", "").strip()
        if not token:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        self.base_url = f"https://api.telegram.org/bot{token}"
        retry = Retry(
            total=3, connect=3, read=2, backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET", "POST"],
            respect_retry_after_header=True,
        )
        self.session = requests.Session()
        self.session.mount("https://", HTTPAdapter(max_retries=retry))

    def send_message(self, text: str, chat_id: str | int | None = None) -> dict:
        target = str(chat_id or self.chat_id).strip()
        if not target:
            raise ValueError("TELEGRAM_CHAT_ID is required for outbound messages")
        return self._post(
            "/sendMessage",
            json={
                "chat_id": target, "text": text, "parse_mode": "HTML",
                "disable_web_page_preview": True,
            },
        )

    def get_updates(self, offset: int | None = None, timeout: int = 30) -> list[dict]:
        params = {"timeout": timeout, "allowed_updates": '["message"]'}
        if offset is not None:
            params["offset"] = offset
        result = self._get("/getUpdates", params=params, timeout=(10, timeout + 10))
        return result.get("result", [])

    def send_document(
        self, path: str | Path, caption: str | None = None,
        reply_to_message_id: int | None = None,
    ) -> dict:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(path)
        data = {"chat_id": self.chat_id}
        if caption:
            data["caption"] = caption[:1024]
            data["parse_mode"] = "HTML"
        if reply_to_message_id is not None:
            data["reply_parameters"] = f'{{"message_id":{reply_to_message_id}}}'
        with path.open("rb") as handle:
            return self._post(
                "/sendDocument", data=data, files={"document": (path.name, handle, "text/markdown")}
            )

    def _post(self, path: str, **kwargs) -> dict:
        try:
            response = self.session.post(
                f"{self.base_url}{path}", timeout=(10, 30), **kwargs
            )
        except requests.Timeout as exc:
            raise RuntimeError("Telegram API timed out after retries") from exc
        except requests.ConnectionError as exc:
            raise RuntimeError("Cannot connect to Telegram API") from exc
        try:
            result = response.json()
        except ValueError:
            result = {"raw_response": response.text}
        if not response.ok:
            raise RuntimeError(
                f"Telegram API error HTTP {response.status_code}: {result}"
            )
        return result

    def _get(self, path: str, **kwargs) -> dict:
        try:
            response = self.session.get(f"{self.base_url}{path}", **kwargs)
        except requests.RequestException as exc:
            raise RuntimeError(f"Telegram API error: {exc}") from exc
        try:
            result = response.json()
        except ValueError:
            result = {"raw_response": response.text}
        if not response.ok or result.get("ok") is False:
            raise RuntimeError(f"Telegram API error HTTP {response.status_code}: {result}")
        return result
