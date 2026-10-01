import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class SnapshotStore:
    def __init__(
        self,
        directory: str = "data/snapshots",
        retention: int = 30,
    ) -> None:
        self.directory = Path(
            directory
        )

        self.retention = retention

        self.directory.mkdir(
            parents=True,
            exist_ok=True,
        )

    def load_latest(
        self,
        project_key: str,
    ) -> dict[str, Any] | None:
        files = self._get_project_files(
            project_key
        )

        if not files:
            return None

        latest_file = files[-1]

        with latest_file.open(
            "r",
            encoding="utf-8",
        ) as file:
            return json.load(
                file
            )

    def load_recent(
        self,
        project_key: str,
        limit: int | None = None,
    ) -> list[dict[str, Any]]:
        files = self._get_project_files(project_key)
        if limit is not None and limit > 0:
            files = files[-limit:]

        snapshots: list[dict[str, Any]] = []
        for path in files:
            with path.open("r", encoding="utf-8") as file:
                snapshots.append(json.load(file))
        return snapshots

    def save(
        self,
        snapshot: dict[str, Any],
    ) -> Path:
        project_key = snapshot[
            "project_key"
        ]

        timestamp = datetime.now(
            timezone.utc
        ).strftime(
            "%Y%m%dT%H%M%S%fZ"
        )

        filename = (
            f"{project_key}_"
            f"{timestamp}.json"
        )

        path = (
            self.directory
            / filename
        )

        with path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                snapshot,
                file,
                indent=2,
                ensure_ascii=False,
            )

        self.cleanup(
            project_key
        )

        return path

    def cleanup(
        self,
        project_key: str,
    ) -> None:
        files = self._get_project_files(
            project_key
        )

        excess = (
            len(files)
            - self.retention
        )

        if excess <= 0:
            return

        for file in files[:excess]:
            file.unlink(
                missing_ok=True
            )

    def count(
        self,
        project_key: str,
    ) -> int:
        return len(
            self._get_project_files(
                project_key
            )
        )

    def _get_project_files(
        self,
        project_key: str,
    ) -> list[Path]:
        files = list(
            self.directory.glob(
                f"{project_key}_*.json"
            )
        )

        return sorted(
            files
        )