from pathlib import Path

from app.logging.run_report import _read_text_file


def test_read_text_file_reads_daily_report(tmp_path: Path) -> None:
    report = tmp_path / "daily.md"
    report.write_text("# Daily Project Report\n\nImportant detail", encoding="utf-8")
    assert _read_text_file(str(report)) == "# Daily Project Report\n\nImportant detail"


def test_read_text_file_missing_is_safe(tmp_path: Path) -> None:
    assert _read_text_file(str(tmp_path / "missing.md")) is None
