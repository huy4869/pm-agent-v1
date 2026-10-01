import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


class GeminiClient:
    def __init__(self) -> None:
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
        self.client = genai.Client(api_key=api_key)

    def generate_json(self, prompt: str, response_schema: dict) -> str:
        config = {
            "response_mime_type": "application/json",
            "response_json_schema": response_schema,
            "temperature": 0.2,
        }

        # Use Chat.send_message rather than direct Models.generate_content.
        # This avoids the SDK's AFC recommendation warning while preserving
        # structured JSON output.
        chat = self.client.chats.create(
            model=self.model,
            config=config,
        )
        response = chat.send_message(prompt)

        if not response.text:
            raise RuntimeError("Gemini returned an empty response")
        return response.text
