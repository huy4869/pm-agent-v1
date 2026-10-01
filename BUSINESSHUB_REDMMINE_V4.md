# BusinessHub Redmine API V4

Endpoints:
- `GET /api/projects`
- `GET /api/projects/{project}/overview?refresh=true|false`
- `GET /api/projects/{project}/issues?filter=overdue|blocked|stale|unassigned|near_due|open|done&versionId=...`
- `GET /api/projects/{project}/versions/{versionId}`

Performance:
- Không tải journal từng issue cho dashboard.
- Snapshot RAM cache mặc định 90 giây (`PM_AGENT_CACHE_SECONDS`).
- Refresh cưỡng bức dùng `refresh=true`.
- Deadline dùng `PM_TIMEZONE=Asia/Ho_Chi_Minh`.
