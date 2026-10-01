# BusinessHub Redmine V4.1 — Cleanup + Risk/Action Engine

## Thay đổi chính

- `Held` / `Pending` được nhận diện là trạng thái **Pending**, không còn bị coi là Blocked hoặc Unassigned mặc định.
- Pending/Held đơn thuần không vào `Task cần chú ý` và không làm xấu health.
- Pending vẫn được cảnh báo nếu có rủi ro độc lập như quá hạn hoặc đang block downstream.
- Bổ sung `pending_issues` và filter `pending` cho API issue.
- Bổ sung Risk/Action Engine deterministic cho project và version; engine chỉ dùng snapshot đã tải, không gọi AI/Redmine thêm.
- Bổ sung action trực tiếp cho overdue, blocked, stale, unassigned, version cận hạn/quá hạn, blocking downstream và workload concentration.
- Cache/snapshot nhanh của V4 được giữ nguyên; journal N+1 không quay lại.
- Thêm `tzdata>=2024.1`; đồng thời có fallback UTC+7 để Windows không làm fail dashboard nếu IANA timezone database bị thiếu.

## API bổ sung dữ liệu

`GET /api/projects/{id}/overview` trả thêm:

- `metrics.pending_issues`
- `riskSummary`
- `actions`

`GET /api/projects/{id}/versions/{versionId}` trả thêm:

- `version.pending`
- `riskSummary`
- `actions`

`GET /api/projects/{id}/issues?filter=pending` lọc Held/Pending.

## Quy tắc quan trọng

Risk/Action trong V4.1 là deterministic, không gọi LLM. AI sẽ được nối sau trên chính snapshot/risk/action này.
