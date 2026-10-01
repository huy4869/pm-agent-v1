# Resource Allocation — AI-first

Resource Allocation dùng AI làm decision/reasoning layer. Code không tính `availability %`, `skill match %` hay `allocation score` để quyết định ai nên nhận task.

## Flow

Telegram question → Jira/Redmine và resource facts → AI prompt → recommendation → Telegram.

Code thu thập và chuẩn hóa assignee, active tasks, status, priority, due date, dependency/signals và resource profile. AI cân nhắc skill, workload, delivery impact và uncertainty.

## Chạy

```bash
cp data/resources.example.json data/resources.json
python main.py bot
```

Ví dụ: `Có task backend khoảng 3 ngày cần bắt đầu ngày mai. Ai làm được?`

Nếu một người không có skill data, AI coi đó là chưa xác minh, không kết luận người đó không có skill.
