import json
import os

import requests


class OpenAICompatibleJSONClient:
    """Small JSON-only client for OpenAI-compatible chat-completions APIs."""

    def __init__(
        self,
        *,
        provider_name: str,
        api_key_env: str,
        model_env: str,
        default_model: str,
        base_url: str,
        timeout_env: str = "AI_REQUEST_TIMEOUT",
        extra_headers: dict[str, str] | None = None,
    ) -> None:
        api_key = os.getenv(api_key_env)
        if not api_key:
            raise ValueError(f"{api_key_env} is not configured")

        self.provider_name = provider_name
        self.api_key = api_key
        self.model = os.getenv(model_env, default_model)
        self.base_url = base_url.rstrip("/")
        self.timeout = float(os.getenv(timeout_env, "45"))
        self.extra_headers = extra_headers or {}

    def generate_json(self, prompt: str, response_schema: dict) -> str:
        # json_object is broadly supported by OpenAI-compatible providers.
        # Put the exact schema in the prompt so the analyst parser receives the
        # same contract regardless of which provider handled the request.
        schema_text = json.dumps(response_schema, ensure_ascii=False)
        final_prompt = (
            f"{prompt}\n\n"
            "STRICT OUTPUT CONTRACT:\n"
            "Return one JSON object only. Do not use markdown fences. "
            "The JSON must conform to this schema:\n"
            f"{schema_text}"
        )

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            **self.extra_headers,
        }
        payload = {
            "model": self.model,
            "messages": [{"role": "user", "content": final_prompt}],
            "temperature": 0.2,
            "response_format": {"type": "json_object"},
        }

        response = requests.post(
            f"{self.base_url}/chat/completions",
            headers=headers,
            json=payload,
            timeout=self.timeout,
        )
        if not response.ok:
            body = response.text[:1200]
            raise RuntimeError(
                f"{self.provider_name} API error HTTP {response.status_code}: {body}"
            )

        data = response.json()
        try:
            content = data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise RuntimeError(
                f"{self.provider_name} returned an invalid chat response"
            ) from exc

        if not content or not str(content).strip():
            raise RuntimeError(f"{self.provider_name} returned an empty response")
        return str(content)
