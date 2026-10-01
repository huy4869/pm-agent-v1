from app.telegram.client import (
    TelegramClient,
)


def main() -> None:
    client = TelegramClient()

    updates = client.get_updates()

    results = updates.get(
        "result",
        []
    )

    if not results:
        print(
            "No Telegram updates found."
        )

        print(
            "Open Telegram, send /start "
            "or any message to your bot, "
            "then run this script again."
        )

        return

    print(
        "=== TELEGRAM CHATS ==="
    )

    seen_chat_ids = set()

    for update in results:
        message = (
            update.get("message")
            or update.get("channel_post")
            or {}
        )

        chat = message.get(
            "chat",
            {}
        )

        chat_id = chat.get(
            "id"
        )

        if not chat_id:
            continue

        if chat_id in seen_chat_ids:
            continue

        seen_chat_ids.add(
            chat_id
        )

        print()

        print(
            "Chat ID:",
            chat_id,
        )

        print(
            "Type:",
            chat.get("type"),
        )

        print(
            "Title:",
            chat.get("title"),
        )

        print(
            "Username:",
            chat.get("username"),
        )

        print(
            "First name:",
            chat.get("first_name"),
        )


if __name__ == "__main__":
    main()