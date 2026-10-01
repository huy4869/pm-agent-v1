from dataclasses import replace
from types import SimpleNamespace
from pathlib import Path

from app.domain.models import ProjectState, ProjectIssue, ProjectIssueState, IssueMetrics, RiskAssessment
from app.metrics.project_metrics import calculate_project_metrics
from app.memory.snapshot_store import SnapshotStore
from app.reports import api_daily
from app.reports.archived_short import archived_short
from app.config import AppConfig
import app.api as api


def snapshot(status="New"):
    issue = ProjectIssue(key="RM-1", summary="Delivery task", status=status, assignee="PM",
        priority=None, issue_type="Task", created_at=None, updated_at=None,
        due_date=None, parent_key=None, dependencies=[], source="redmine")
    state = ProjectState(project_key="65", issues=[ProjectIssueState(issue=issue,
        metrics=IssueMetrics(None, None, None), signals=[], risk=RiskAssessment("LOW", []))])
    state.metrics = calculate_project_metrics(state)
    return {"state": state, "project": {"identifier": "demo"}, "client": SimpleNamespace(base_url="https://example.test"),
            "syncedAt": status, "versions": [], "issues": []}


import unittest
from tempfile import TemporaryDirectory
from unittest.mock import patch


class DailyReportApiTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory(dir=Path(__file__).resolve().parent)
        self.addCleanup(self.temp.cleanup)

    def patch(self, target, attribute, value):
        replacement = patch.object(target, attribute, value)
        replacement.start()
        self.addCleanup(replacement.stop)

    def test_archives_compare_prior_snapshot_and_do_not_overwrite(self):
        tmp_path = Path(self.temp.name)
        config = replace(AppConfig(), snapshot_directory=str(tmp_path / "snapshots"),
                         daily_report_directory=str(tmp_path / "reports"))
        self.patch(api_daily, "AppConfig", lambda: config)
        first = snapshot()
        first_name = api_daily.archive_api_snapshot(first)
        assert api_daily.archive_api_snapshot(first) == first_name
        store = SnapshotStore(config.snapshot_directory)
        assert len(store.load_recent("demo")) == 1
        second = snapshot("Closed")
        second_name = api_daily.archive_api_snapshot(second)
        assert second_name != first_name
        history = store.load_recent("demo")
        assert len(history) == 2
        assert history[-1]["issues"]["RM-1"]["status"] == "Closed"
        report = Path(config.daily_report_directory) / "demo" / second_name
        short = archived_short(report, "demo", report.read_text(encoding="utf-8"))
        assert "baseline" not in short.lower()
        assert "Risk Lifecycle" in short
        assert "1 hoàn thành" in short
        assert "100% hoàn tất" in short


    def test_generate_endpoint_requests_fresh_snapshot_and_ai(self):
        calls = []
        self.patch(api, "_load_snapshot", lambda project_id, refresh=False: calls.append(refresh) or snapshot())
        self.patch(api, "archive_api_snapshot", lambda snap, include_ai=False: calls.append(include_ai) or "demo_Daily_Report_new.md")
        self.patch(api, "project_daily_reports", lambda identifier: {"items": [], "report": None})
        self.patch(api, "analyze_redmine_snapshot", lambda *args: (_ for _ in ()).throw(AssertionError("AI called")))
        result = api.generate_project_daily_report("65")
        assert calls == [True, True]
        assert result["generatedFilename"] == "demo_Daily_Report_new.md"


    def test_ai_refresh_fetches_new_snapshot_but_cached_read_does_not_regenerate(self):
        calls = []
        analyzed = []
        sample = snapshot()
        self.patch(api, "_load_snapshot", lambda project_id, refresh=False: calls.append(refresh) or sample)
        self.patch(api, "archive_api_snapshot", lambda snap: "saved.md")
        self.patch(api, "analyze_redmine_snapshot", lambda *args: analyzed.append(True) or {"health": "GREEN"})
        self.patch(api, "_INTELLIGENCE_CACHE", {})
        api.project_intelligence("demo", False)
        api.project_intelligence("demo", False)
        api.project_intelligence("demo", True)
        assert calls == [False, False, True]
        assert len(analyzed) == 2
