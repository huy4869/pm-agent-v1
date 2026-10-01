# Triển khai PM Agent — port 8090

PM Agent chạy Docker riêng trên cùng VPS, dùng chung network hiện tại của Hub.
Không publish 8090 ra Internet. Hub gọi server-side: PM_AGENT_BASE_URL=http://pm-agent:8090.
VPS phải truy cập được Redmine và các AI provider; nếu Redmine yêu cầu VPN, phải kết nối VPN trước.

## Chuẩn bị

Đặt source tại /home/pm-agent. Thư mục local hiện chưa có Git repository riêng.
Xem tên network hiện tại (chọn network có Hub và DB):

```bash
docker inspect businesshub_app --format '{{json .NetworkSettings.Networks}}'
```

Tạo /home/pm-agent/.env từ .env.example và điền secrets trên VPS:

```env
PM_SOURCE=redmine
REDMINE_BASE_URL=https://your-redmine.example.com
REDMINE_API_KEY=your-secret
AI_PROVIDER_ORDER=groq,gemini,openrouter
GROQ_API_KEY=your-secret
# Điền thêm Gemini/OpenRouter nếu dùng fallback.
REPORT_LANGUAGE=vi
REPORT_TIMEZONE=Asia/Ho_Chi_Minh
PM_TIMEZONE=Asia/Ho_Chi_Minh
# Thay bằng tên network thực tế lấy từ docker inspect.
BUSINESSHUB_DOCKER_NETWORK=businesshub_businesshub-network
```

Biến URL chính xác là REDMINE_BASE_URL, không phải REDMINE_URL trong tài liệu cũ.
Không đưa .env hoặc data vào image/repo; API không cần Telegram.

## Triển khai lần đầu

```bash
cd /home/pm-agent
docker compose config --quiet
docker compose up -d --build pm-agent
docker compose ps
docker compose logs --tail=100 pm-agent
docker compose exec -T pm-agent python -c "import urllib.request; print(urllib.request.urlopen('http://127.0.0.1:8090/health').read().decode())"
```

Healthcheck dùng Python vì python:slim không có curl sẵn. Chạy một worker; không --reload trên production.

## Nối Hub

Thêm vào /home/businesshub/.env:

```env
PM_AGENT_BASE_URL=http://pm-agent:8090
```

Recreate app để nhận env mới:

```bash
cd /home/businesshub
docker compose up -d --force-recreate app
docker exec businesshub_app node -e "fetch('http://pm-agent:8090/health').then(async r=>{if(!r.ok)throw Error(r.status);console.log(await r.text())}).catch(e=>{console.error(e.message);process.exit(1)})"
```

Không dùng localhost trong container Hub, vì đó là chính Hub. Không cần Prisma migration cho kết nối này.

## Giữ snapshot / báo cáo

Volume pm-agent-data mount /app/data, giữ snapshots, daily_reports và logs khi recreate container.
Không chạy docker compose down -v nếu cần giữ lịch sử.
Dữ liệu local không tự lên VPS. Nếu cần giữ baseline cũ, sao chép data vào volume trước khi chạy báo cáo mới và cấp quyền ghi cho UID 10001.
RAM cache mất khi restart; snapshot trên volume vẫn còn.

## CI/CD sau merge main

Nên dùng repository, image và pipeline riêng cho PM Agent; Hub giữ workflow hiện tại.
Luồng: push main -> kiểm thử -> build/push GHCR với tag SHA -> SSH VPS -> pull -> up -d pm-agent -> healthcheck.
Secrets: VPS_HOST, VPS_USER, VPS_SSH_KEY, VPS_PORT; environment production.
Khi đã có image GHCR, đặt PM_AGENT_IMAGE=ghcr.io/<owner>/<repo>:<sha> trong .env trên VPS:

```bash
cd /home/pm-agent
docker compose pull pm-agent
docker compose up -d --no-build pm-agent
```

VPS cần quyền pull private GHCR. Rollback bằng tag SHA trước, giữ nguyên volume.
Cần xác định repo PM Agent trước khi tạo workflow cụ thể. Chưa deploy VPS trong lần chuẩn bị này.

## Local 8090

```cmd
.venv\Scripts\activate
uvicorn app.api:app --host 127.0.0.1 --port 8090 --reload
```

Hub local dùng PM_AGENT_BASE_URL=http://127.0.0.1:8090 rồi restart npm run dev.
Hub production dùng PM_AGENT_BASE_URL=http://pm-agent:8090.
