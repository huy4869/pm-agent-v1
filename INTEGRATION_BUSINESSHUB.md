# PM Agent ↔ BusinessHub (V1)

PM Agent chạy API nội bộ; BusinessHub proxy API này và giữ UI/auth.

## Chạy PM Agent

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`.env` cần tối thiểu:

```env
PM_SOURCE=redmine
REDMINE_BASE_URL=https://redmine.example.com
REDMINE_API_KEY=...
```

API mode không bắt buộc `REDMINE_PROJECT_ID`; project id được BusinessHub truyền theo request.

```bash
uvicorn app.api:app --host 127.0.0.1 --port 8000 --reload
```

Kiểm tra: `GET http://127.0.0.1:8000/health`.
