# PM Agent

PM Agent đọc dữ liệu dự án từ Redmine/Jira, phân tích rủi ro giao hàng bằng AI và lưu lịch sử để so sánh giữa các lần chạy. BusinessHub sử dụng API Redmine của Agent cho Daily Report, AI Observations và chatbot dự án.

Luồng tích hợp: **BusinessHub → PM Agent → Redmine / nhà cung cấp AI**. API key nằm ở server PM Agent.

## Chạy local

python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.api:app --host 127.0.0.1 --port 8000 

Yêu cầu Python 3.12. Tạo môi trường và cài dependencies trên Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Copy-Item .env.example .env
```

Trên Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
cp .env.example .env
```

Sửa `.env` bằng thông tin thực tế, tối thiểu cho tích hợp Hub:

```dotenv
PM_SOURCE=redmine
REDMINE_BASE_URL=https://redmine.example.com
REDMINE_API_KEY=replace_me
REDMINE_PROJECT_ID=1
AI_PROVIDER_ORDER=groq,gemini,openrouter
GROQ_API_KEY=replace_me
REPORT_LANGUAGE=vi
REPORT_TIMEZONE=Asia/Ho_Chi_Minh
PM_TIMEZONE=Asia/Ho_Chi_Minh
PM_AGENT_CACHE_SECONDS=90
```

Điền key và model cho các provider sử dụng theo `.env.example`. API lấy dự án từ ID trên URL; `REDMINE_PROJECT_ID` dùng cho luồng CLI. API Redmine hiện tại không chuyển sang Jira khi thay `PM_SOURCE`.

Khởi động API, nạp `.env` rõ ràng:

```bash
python -m uvicorn app.api:app --host 0.0.0.0 --port 8090 --workers 1 --env-file .env
```

- Health: `http://127.0.0.1:8090/health`
- Swagger: `http://127.0.0.1:8090/docs`
- Đặt `PM_AGENT_BASE_URL=http://127.0.0.1:8090` trong `.env` của BusinessHub, rồi khởi động lại Hub.

## Docker

`Dockerfile` chạy API trên **8090**, dùng user không có quyền root và một worker. Image có healthcheck; dữ liệu nằm trong `/app/data`. Container này chạy API; các lệnh CLI/Telegram bên dưới chạy từ source local.

Build và chạy độc lập để kiểm tra local:

```bash
docker build -t pm-agent:local .
docker run -d --name pm-agent --env-file .env -p 127.0.0.1:8090:8090 -v pm-agent-data:/app/data pm-agent:local
docker logs --tail 100 pm-agent
```

Deploy cùng Hub bằng `docker-compose.yml`: thêm vào `.env` tên Docker network thực tế mà container Hub đang sử dụng:

```dotenv
BUSINESSHUB_DOCKER_NETWORK=replace_with_existing_hub_network
```

```bash
docker compose config --quiet
docker compose up -d --build
docker compose ps
docker compose logs --tail 100 pm-agent
```

Trong cấu hình Hub trên VPS, đặt `PM_AGENT_BASE_URL=http://pm-agent:8090` rồi tạo lại container Hub để nạp biến mới. Compose dùng network chung và không publish port ra ngoài. API cần nằm trong mạng nội bộ vì chưa có lớp xác thực riêng; Hub kiểm tra quyền người dùng trước khi gọi API.

Volume `pm-agent-data` giữ snapshots và báo cáo qua các lần tạo lại container. Không dùng `docker compose down -v` nếu cần giữ lịch sử. Khi chuyển dữ liệu cũ vào volume, đảm bảo user UID/GID `10001` có quyền ghi.

Xem hướng dẫn đầy đủ tại [Deploy PM Agent port 8090](docs/PM_Agent_Deployment_8090.md).

## Daily Report, AI Observations và chatbot

| Thao tác trong Hub | Hành vi của Agent |
| --- | --- |
| Xem Daily Report hoặc tải file | Đọc báo cáo đã lưu, không gọi AI |
| Bấm Làm mới Daily Report | Đọc mới Redmine, gọi AI, lưu báo cáo và snapshot mới |
| Vào phần phân tích AI lần đầu | Phân tích AI; có cache ở server |
| Chuyển tab rồi quay lại trong cùng trang | Hub giữ kết quả đã lấy |
| Bấm Phân tích lại | Đọc mới Redmine và gọi lại AI |
| Mở khung chatbot | Chưa gọi AI |
| Gửi câu hỏi chatbot | Gọi AI với dữ liệu dự án và lịch sử hội thoại giới hạn |

Daily Report hiển thị bản short trước; chọn **Detailed Daily Report** để xem bản đầy đủ. Link tên file tải báo cáo Markdown. Refresh tạo snapshot mới ngay cả khi dữ liệu không đổi; `Since Last Run` so sánh với snapshot trước đó. Lần đầu chưa có lịch sử sẽ hiển thị baseline.

Khi AI lỗi hoặc hết quota, Daily Report vẫn có thể lưu kết quả theo dữ liệu/rule và trả `aiStatus=unavailable`. Chatbot trả lời dự phòng và báo rõ. Vì vậy bấm làm mới không bảo đảm nội dung thay đổi nếu dữ liệu Redmine vẫn như cũ.

Chatbot nổi ở góc phải dưới các trang dự án Redmine trong Hub, có ba câu hỏi gợi ý về tình hình dự án, task ưu tiên và người có thể nhận task gấp. AI dùng ngữ cảnh được giới hạn và đối chiếu mã issue; dữ liệu tải công việc không đủ để khẳng định kỹ năng hay khả năng nhận việc của một người. Chatbot không tự giao việc hoặc sửa task.

## API

| Method | Endpoint | Mục đích |
| --- | --- | --- |
| GET | `/health` | Kiểm tra API |
| GET | `/api/projects` | Danh sách dự án Redmine |
| GET | `/api/projects/{id}/overview` | Tổng quan dự án |
| GET | `/api/projects/{id}/issues` | Danh sách task/issue |
| GET | `/api/projects/{id}/versions/{version_id}` | Chi tiết version |
| GET | `/api/projects/{id}/intelligence` | Phân tích AI; `refresh=true` để phân tích lại |
| GET | `/api/projects/{id}/daily-reports` | Danh sách báo cáo; `filename` để đọc bản cụ thể |
| POST | `/api/projects/{id}/daily-reports` | Quét mới, phân tích AI và lưu snapshot/báo cáo |
| POST | `/api/projects/{id}/chat` | Hỏi đáp theo dự án |

Ví dụ body chatbot:

```json
{
  "message": "Task nào cần ưu tiên xử lý hôm nay?",
  "history": []
}
```

`message` tối đa 2.000 ký tự; `history` tối đa 8 tin nhắn với `role` là `user` hoặc `assistant`. Xem Swagger để biết tham số và cấu trúc response đầy đủ.

## Lưu trữ và cache

Mặc định khi chạy từ source:

- `data/snapshots/`: snapshot để so sánh thay đổi và theo dõi vòng đời rủi ro.
- `data/daily_reports/<project>/`: báo cáo `.md` và bản short `.short.html`.
- `data/logs/<project>/`: log của luồng chạy báo cáo CLI.

Có thể đổi đường dẫn và thời gian giữ dữ liệu qua `.env.example`. Snapshot phục vụ API được cache trong RAM mặc định 90 giây; lịch sử trên đĩa là dữ liệu riêng, không mất khi restart nếu volume còn nguyên. Dùng một worker với cơ chế cache hiện tại.

## Chạy báo cáo CLI và Telegram

Từ source với môi trường Python đã kích hoạt và `.env` đã cấu hình:

```bash
python main.py
python main.py bot
```

Lệnh đầu chạy pipeline Daily Report, lưu lịch sử và gửi Telegram theo cấu hình. Lệnh `bot` chạy hỏi đáp Telegram bằng long polling, khác với chatbot web của Hub. CLI hỗ trợ Jira hoặc Redmine theo `PM_SOURCE`. Automation riêng của dự án nằm trong `projects/`, trong đó BCY/SPMM nằm ở `projects/bcy_spmm/`.

Xem [Resource Allocation](docs/RESOURCE_ALLOCATION.md) để cấu hình hồ sơ kỹ năng cho luồng Telegram.

## Kiểm tra

Hai nhóm kiểm tra tập trung cho lưu báo cáo/snapshot và chatbot:

```bash
python -m unittest discover -s tests -p test_api_daily_reports.py
python -m unittest discover -s tests -p test_project_chat.py
```

Xem [Testing](docs/TESTING.md) cho chiến lược kiểm thử rộng hơn. Các unit test không thay thế việc kiểm tra kết nối Redmine, provider AI và Docker thực tế trên VPS.

## Tài liệu thiết kế

Dữ liệu nguồn → facts/guardrails → AI reasoning → báo cáo → kênh hiển thị. Lớp deterministic bảo vệ tính đúng của dữ liệu; đánh giá AI có thể khác mức áp lực theo rule nếu ngữ cảnh giao hàng hỗ trợ.

- [Architecture](docs/ARCHITECTURE.md)
- [AI Design](docs/AI_DESIGN.md)
- [Risk Engine](docs/RISK_ENGINE.md)
- [Report Specification](docs/REPORT_SPEC.md)
- [Configuration](docs/CONFIGURATION.md)
- [Operations](docs/OPERATIONS.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](CHANGELOG.md)

Không commit `.env`, API key, Telegram token hoặc dữ liệu dự án nhạy cảm. `.dockerignore` loại `.env` và dữ liệu local khỏi build context; credentials được truyền lúc chạy container.
