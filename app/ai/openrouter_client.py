import os

from app.ai.openai_compatible_client import OpenAICompatibleJSONClient


class OpenRouterClient(OpenAICompatibleJSONClient):
    def __init__(self) -> None:
        headers = {}
        site_url = os.getenv("OPENROUTER_SITE_URL")
        app_name = os.getenv("OPENROUTER_APP_NAME", "PM Agent")
        if site_url:
            headers["HTTP-Referer"] = site_url
        if app_name:
            headers["X-Title"] = app_name

        super().__init__(
            provider_name="OpenRouter",
            api_key_env="OPENROUTER_API_KEY",
            model_env="OPENROUTER_MODEL",
            default_model="openai/gpt-oss-120b:free",
            base_url="https://openrouter.ai/api/v1",
            extra_headers=headers,
        )
