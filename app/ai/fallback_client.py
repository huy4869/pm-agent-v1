from dataclasses import dataclass
from typing import Callable


@dataclass(frozen=True)
class AIProviderSpec:
    name: str
    factory: Callable[[], object]


class FallbackAIClient:
    """Try AI providers in order and fail only after every provider failed.

    Provider construction is lazy. A missing fallback API key therefore does
    not prevent the primary provider from being used.
    """

    def __init__(self, providers: list[AIProviderSpec]) -> None:
        if not providers:
            raise ValueError("At least one AI provider is required")
        self.providers = providers
        self.last_provider: str | None = None
        self.failures: list[str] = []

    def generate_json(self, prompt: str, response_schema: dict) -> str:
        self.last_provider = None
        self.failures = []

        for spec in self.providers:
            try:
                client = spec.factory()
                result = client.generate_json(prompt, response_schema)
                self.last_provider = spec.name
                return result
            except Exception as exc:
                self.failures.append(f"{spec.name}: {type(exc).__name__}: {exc}")
                print(f"⚠ AI provider {spec.name} failed; trying next fallback")

        raise RuntimeError("All AI providers failed — " + " | ".join(self.failures))
