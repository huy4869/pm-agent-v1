# BCY SPMM Redmine scripts

These scripts use the Redmine connection configured in the repository `.env`.
Credentials are never stored in this directory.

List active tasks and show project statistics:

```bash
.venv/bin/python scripts/redmine/list_tasks.py
```

Useful filters:

```bash
.venv/bin/python scripts/redmine/list_tasks.py --all
.venv/bin/python scripts/redmine/list_tasks.py --status "In Progress"
.venv/bin/python scripts/redmine/list_tasks.py --assignee "Member name"
.venv/bin/python scripts/redmine/list_tasks.py --format json
```
