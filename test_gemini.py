from app.ai.gemini_client import GeminiClient


def main() -> None:
    client = GeminiClient()

    response = client.generate(
        """
You are a software project manager.

Respond with exactly one sentence.

A Jira issue is overdue by 1 day and is
blocking two downstream issues.

What should the project manager do?
"""
    )

    print("\n=== GEMINI RESPONSE ===")
    print(response)


if __name__ == "__main__":
    main()