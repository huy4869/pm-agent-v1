import os

from app.ai.fallback_client import AIProviderSpec, FallbackAIClient
from app.ai.gemini_client import GeminiClient
from app.ai.groq_client import GroqClient
from app.ai.openrouter_client import OpenRouterClient


def build_ai_client() -> FallbackAIClient:
    """Build provider chain.

    Default order requested for PM Agent:
      Groq -> Gemini -> OpenRouter -> deterministic report fallback.

    AI_PROVIDER_ORDER can override the first three, e.g.
    AI_PROVIDER_ORDER=groq,gemini,openrouter
    """
    factories = {
        "groq": AIProviderSpec("Groq", GroqClient),
        "gemini": AIProviderSpec("Gemini", GeminiClient),
        "openrouter": AIProviderSpec("OpenRouter", OpenRouterClient),
    }

    raw_order = os.getenv("AI_PROVIDER_ORDER", "groq,gemini,openrouter")
    names = [item.strip().lower() for item in raw_order.split(",") if item.strip()]
    providers = []
    seen = set()
    for name in names:
        if name not in factories:
            raise ValueError(
                f"Unknown AI provider '{name}' in AI_PROVIDER_ORDER. "
                "Allowed: groq, gemini, openrouter"
            )
        if name not in seen:
            providers.append(factories[name])
            seen.add(name)

    return FallbackAIClient(providers)
