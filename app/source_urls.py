import os


def source_name() -> str:
    return os.getenv("PM_SOURCE", "jira").strip().lower()


def issue_url(issue_key: str, base_url: str | None = None) -> str:
    source = source_name()
    base = base_url or os.getenv("REDMINE_BASE_URL" if source == "redmine" else "JIRA_BASE_URL")
    if not base:
        raise ValueError(f"Missing {'REDMINE_BASE_URL' if source == 'redmine' else 'JIRA_BASE_URL'}")
    if source == "redmine":
        return f"{base.rstrip('/')}/issues/{issue_key.removeprefix('RM-')}"
    return f"{base.rstrip('/')}/browse/{issue_key}"


def project_url(project_key: str, base_url: str | None = None) -> str:
    source = source_name()
    base = base_url or os.getenv("REDMINE_BASE_URL" if source == "redmine" else "JIRA_BASE_URL")
    if not base:
        raise ValueError("Missing source base URL")
    if source == "redmine":
        return f"{base.rstrip('/')}/projects/{project_key}/issues"
    return f"{base.rstrip('/')}/jira/software/projects/{project_key}"
