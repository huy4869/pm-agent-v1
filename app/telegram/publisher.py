from pathlib import Path

from app.telegram.client import TelegramClient


class TelegramPublisher:
    def __init__(self, client: TelegramClient) -> None:
        self.client = client

    def publish(self, message: str, attachment: str | Path | None = None) -> None:
        result = self.client.send_message(message)
        if attachment is not None:
            self.client.send_document(
                attachment,
                reply_to_message_id=result.get("result", {}).get("message_id"),
            )
