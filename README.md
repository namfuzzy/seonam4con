# SEO nội bộ – Nền tảng quản trị đa dự án

Ứng dụng full-stack (FastAPI + Next.js) hỗ trợ đội SEO quản lý hiệu suất nhiều dự án, đồng bộ dữ liệu chính thống (GSC, PSI) và kết nối WordPress/IndexNow/Gemini thông qua giao diện tiếng Việt. Toàn bộ API key nhập từ UI và lưu mã hoá bằng AES-256 (khoá lấy từ biến môi trường `APP_SECRET`).

## Kiến trúc tổng quan

```mermaid
graph LR
  subgraph Frontend (Vercel)
    A[Next.js App Router]
  end
  subgraph Backend (Render/Railway)
    B[FastAPI]
    C[Worker/Cron Endpoint]
  end
  subgraph Data
    D[(PostgreSQL - Neon/Supabase)]
    E[(Upstash Redis - tuỳ chọn)]
  end
  A <-- TanStack Query --> B
  B <-- Alembic / SQLAlchemy --> D
  C --> B
  B -->|OAuth| F[(GSC API)]
  B -->|REST| G[(PageSpeed Insights)]
  B -->|REST| H[(WordPress)]
  B -->|HTTPS| I[(IndexNow)]
  B -->|REST| J[(Gemini API)]
```

## ERD cơ sở dữ liệu (PostgreSQL)

```mermaid
erDiagram
    users ||--o{ projects : "sở hữu"
    projects ||--o{ sites : "bao gồm"
    sites ||--o{ integrations : "tích hợp"
    integrations ||--o{ credentials : "mã hoá"
    sites ||--o{ pages : "giám sát"
    pages ||--o{ page_metrics : "GSC"
    pages ||--o{ cwv_metrics : "PSI"
    sites ||--o{ suggestions : "gợi ý"
    sites ||--o{ content_briefs : "brief"
    sites ||--o{ content_drafts : "nháp"
    pages ||--o{ internal_links : "liên kết"
    pages ||--o{ linkscore : "điểm"
    projects ||--o{ alerts : "cảnh báo"
    projects ||--o{ logs : "audit"
```

## Yêu cầu hệ thống

- Python 3.12+
- Node.js 18+
- PostgreSQL 15 (Neon/Supabase free tier)
- (Tuỳ chọn) Upstash Redis free nếu cần cache

## Chuẩn bị biến môi trường

Tạo file `.env` tại thư mục gốc dựa trên `.env.sample`:

```bash
cp .env.sample .env
```

Điền các biến quan trọng:

- `APP_SECRET`: khoá 32 byte (ví dụ sinh qua `openssl rand -hex 16`).
- `DATABASE_URL`: chuỗi kết nối Postgres dạng `postgresql+asyncpg://user:pass@host/db`.
- `SECRET_KEY`: khoá ký JWT.
- `BACKEND_CORS_ORIGINS`: URL frontend (ví dụ `http://localhost:3000`).
- `NEXT_PUBLIC_API_BASE`: địa chỉ backend cho frontend.
- `NEXT_PUBLIC_DEMO_TOKEN`: (tuỳ chọn) JWT để frontend truy cập nhanh môi trường demo.

## Thiết lập backend FastAPI

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
python seed.py  # tạo user & dữ liệu demo
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Tài khoản demo

- Email: `admin@example.com`
- Mật khẩu: `Admin123!`

API docs: `http://localhost:8000/api/v1/openapi.json` (Swagger UI tự động từ FastAPI).

## Thiết lập frontend Next.js

```bash
cd frontend
npm install
npm run dev
```

Truy cập `http://localhost:3000`. UI tiếng Việt, dark mode, TanStack Query + Zustand quản lý state dự án, hiển thị KPI, danh sách dự án, site và thẻ tích hợp (mask thông tin khoá).

## Triển khai free-tier đề xuất

| Tầng | Dịch vụ | Ghi chú |
| --- | --- | --- |
| Frontend | **Vercel** (Next.js) | Build command `npm run build`, env `NEXT_PUBLIC_API_BASE` trỏ tới backend. |
| Backend API | **Render** (Free Web Service) hoặc **Railway** | Start command `uvicorn app.main:app --host 0.0.0.0 --port $PORT`. Thiết lập biến môi trường giống `.env`. |
| CSDL | **Neon** hoặc **Supabase** | Sao chép connection string vào `DATABASE_URL`. |
| Cron/Scheduler | Render Cron Job hoặc Railway Scheduled Task | Gọi webhook `POST /api/v1/cron/daily` (định nghĩa thêm) để kéo dữ liệu. |
| Cache | Upstash Redis (tuỳ chọn) | Lưu queue/caching nếu mở rộng. |

### Quy trình triển khai

1. Tạo database trên Neon/Supabase, bật SSL.
2. Deploy backend lên Render/Railway, cấu hình biến môi trường (không lưu API key thật trong code).
3. Chạy `alembic upgrade head` và `python seed.py` thông qua job "Shell" của Render/Railway.
4. Deploy frontend lên Vercel, nhập biến `NEXT_PUBLIC_API_BASE`, `NEXT_PUBLIC_DEMO_TOKEN` nếu muốn auto login.
5. Cập nhật DNS/Domain tuỳ nhu cầu.

## Lịch cron & tác vụ nền

- Tạo job hằng ngày (`0 7 * * *`) trên Render Scheduler hoặc GitHub Actions gọi webhook backend `/api/v1/cron/daily` để đồng bộ GSC/PSI, phát hiện cảnh báo.
- (Tuỳ chọn) Tạo job hàng tuần `/api/v1/cron/weekly` cho phân tích decay.

## Bảo mật & mã hoá

- Credentials lưu trong bảng `credentials` với cột `value_encrypted` (AES-256-GCM). Chỉ giải mã khi người dùng có quyền và yêu cầu "Hiện tạm thời".
- JWT (HS256) cho đăng nhập; refresh token thời hạn 7 ngày.
- Ghi log thao tác tại bảng `logs` phục vụ audit.

## Kiểm thử

### Backend

```bash
cd backend
pytest
```

### Frontend

```bash
cd frontend
npm run lint
```

## Lộ trình mở rộng

- Bổ sung OAuth flow GSC, đồng bộ PSI, WordPress draft publish.
- Tính toán LinkScore (PageRank + GSC + similarity) và gợi ý internal link.
- Module Gemini (khi user nhập key) cho brief → outline → draft → schema.
- Cron tự động gửi cảnh báo rớt CTR/CWV, hỗ trợ email.
