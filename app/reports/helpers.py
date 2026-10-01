from html import escape

from app.source_urls import issue_url


def issue_ref(
    issue_key: str,
) -> str:
    url = issue_url(issue_key)

    return (
        f'<a href="{escape(url)}">'
        f"{escape(issue_key)}"
        "</a>"
    )


def signal_codes(
    state,
) -> set[str]:
    return {
        signal.code
        for signal in state.signals
    }


def blocking_targets(
    issue,
) -> list[str]:
    return [
        dependency.related_issue_key
        for dependency in issue.dependencies or []
        if dependency.relation.lower() == "blocks"
    ]


def unique(
    items: list[str],
) -> list[str]:
    return list(
        dict.fromkeys(items)
    )
