# BCY Redmine scripts

- `create_redmine_sample_task.py`: creates the original sample issue and avoids duplicates.
- `setup_redmine_spmm_hierarchy.py`: creates or updates the BCY Epic, Feature, BA/DEV/TEST tasks, and blocking relations.

Run from the repository root:

```powershell
.\.venv\Scripts\python.exe projects\bcy_spmm\setup_redmine_spmm_hierarchy.py
```
# Google Drive master-control sync

The reusable synchronization entry point is `sync_master_control.py`. Codex
reads `BCY - Master control` / `Thông tin chung`, writes the current rows to
`master_control_snapshot.json`, previews changes, and then runs:

```powershell
.\.venv\Scripts\python.exe projects\bcy_spmm\sync_master_control.py --apply
```

The snapshot schema is documented in `master_control_snapshot.example.json`.
Blank source cells preserve Redmine data. The script never edits description
or priority and never creates missing issues.
