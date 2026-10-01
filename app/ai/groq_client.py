from app.ai.openai_compatible_client import OpenAICompatibleJSONClient


class GroqClient(OpenAICompatibleJSONClient):
    def __init__(self) -> None:
        super().__init__(
            provider_name="Groq",
            api_key_env="GROQ_API_KEY",
            model_env="GROQ_MODEL",
            default_model="openai/gpt-oss-120b",
            base_url="https://api.groq.com/openai/v1",
        )
