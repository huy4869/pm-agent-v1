import unittest

from app.ai.fallback_client import AIProviderSpec, FallbackAIClient


class FakeClient:
    def __init__(self, result=None, error=None):
        self.result = result
        self.error = error

    def generate_json(self, prompt, response_schema):
        if self.error:
            raise self.error
        return self.result


class FallbackAIClientTests(unittest.TestCase):
    def test_uses_next_provider_after_failure(self):
        client = FallbackAIClient([
            AIProviderSpec("Groq", lambda: FakeClient(error=RuntimeError("429"))),
            AIProviderSpec("Gemini", lambda: FakeClient(result='{"health":"OK"}')),
            AIProviderSpec("OpenRouter", lambda: FakeClient(result='{}')),
        ])
        result = client.generate_json("x", {})
        self.assertEqual(result, '{"health":"OK"}')
        self.assertEqual(client.last_provider, "Gemini")
        self.assertEqual(len(client.failures), 1)

    def test_raises_only_after_all_fail(self):
        client = FallbackAIClient([
            AIProviderSpec("Groq", lambda: FakeClient(error=RuntimeError("a"))),
            AIProviderSpec("Gemini", lambda: FakeClient(error=RuntimeError("b"))),
            AIProviderSpec("OpenRouter", lambda: FakeClient(error=RuntimeError("c"))),
        ])
        with self.assertRaisesRegex(RuntimeError, "All AI providers failed"):
            client.generate_json("x", {})
        self.assertEqual(len(client.failures), 3)


if __name__ == "__main__":
    unittest.main()
