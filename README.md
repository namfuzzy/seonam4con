# SEO Nội Bộ – Nền tảng SEO all-in-one cho đội marketing

> MVP v1.0 đáp ứng yêu cầu quản lý đa dự án, tích hợp Google Search Console, PageSpeed Insights, WordPress, IndexNow, Gemini (tùy chọn) với chi phí 0đ (free-tier). Toàn bộ giao diện tiếng Việt, dark mode, dữ liệu lưu tại PostgreSQL và thông tin nhạy cảm được mã hoá AES-256.

## Kiến trúc tổng thể

```mermaid
graph TD
  subgraph Frontend (Vercel / Next.js)
    UI[UI App Router]
    State[Zustand Store]
    Query[React Query]
  end

  subgraph Backend (Render/Railway / FastAPI)
    API[REST API]
    Worker[Cron & Background]
  end

  subgraph Data Layer
    DB[(PostgreSQL - Neon/Supabase)]
    Cache[(Upstash Redis - tùy chọn)]
  end

  subgraph Integrations
    GSC[Google Search Console]
    PSI[PageSpeed Insights]
    WP[WordPress REST]
    IDX[IndexNow]
    GEM[Gemini API]
  end

  UI -->|JWT| API
  API -->|SQLAlchemy| DB
  API -->|Cache| Cache
  API --> GSC
  API --> PSI
  API --> WP
  API --> IDX
  API --> GEM
  Worker --> API
```

### ERD cơ sở dữ liệu (PostgreSQL)

```mermaid
erDiagram
  users ||--o{ projects : ""
  projects ||--o{ sites : ""
  sites ||--o{ pages : ""
  projects ||--o{ integrations : ""
  integrations ||--o{ credentials : ""
  sites ||--o{ gsc_sites : ""
  pages ||--o{ page_metrics : ""
  pages ||--o{ cwv_metrics : ""
  pages ||--o{ internal_links : from
  pages ||--o{ internal_links : to
  pages ||--o{ linkscore : ""
  sites ||--o{ suggestions : ""
  sites ||--o{ content_briefs : ""
  sites ||--o{ content_drafts : ""
  projects ||--o{ alerts : ""
  projects ||--o{ logs : ""
```

## Thư mục & thành phần chính

```
.
├── backend              # FastAPI + SQLAlchemy + Alembic + seed + cron stub
│   ├── app
│   │   ├── api/v1       # Routers (auth, projects, sites, integrations, metrics, health)
│   │   ├── core         # Config, security (JWT, password hash)
│   │   ├── db           # Session & Base
│   │   ├── models       # ORM models theo bảng yêu cầu
│   │   ├── schemas      # Pydantic schemas
│   │   ├── utils        # AES-256 encryption helper
│   │   ├── background   # Cron hook mẫu
│   │   └── tests        # Pytest mẫu
│   ├── alembic          # Migration scripts (0001_initial)
│   ├── requirements.txt
│   └── seed.py          # Tạo dữ liệu demo
├── frontend             # Next.js 14 App Router, TailwindCSS, Zustand, React Query
│   ├── app              # Pages: landing, dashboard, dự án, tabs tổng quan & tích hợp
│   ├── components       # UI card, table, form tích hợp
│   ├── lib              # API client
│   ├── store            # Zustand store demo
│   ├── styles           # Tailwind global dark theme
│   ├── package.json
│   └── tailwind.config.ts
└── .env.sample          # Biến môi trường cần khi deploy
```

## Hướng dẫn triển khai (free-tier)

### 1. PostgreSQL (Neon hoặc Supabase)
1. Tạo project miễn phí tại [https://neon.tech](https://neon.tech) (hoặc Supabase).
2. Lấy connection string dạng `postgresql://USER:PASSWORD@HOST/DB`.
3. Cập nhật `.env` cho backend (`DATABASE_URL`).

### 2. Backend FastAPI trên Render/Railway
1. Fork repo, kết nối Render/Railway với GitHub.
2. Tạo dịch vụ web mới:
   - Build command: `pip install -r requirements.txt`
   - Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - Environment variables:
     | KEY | VALUE |
     | --- | --- |
     | `APP_SECRET` | Chuỗi ngẫu nhiên ≥ 32 ký tự (mã hoá AES-256) |
     | `JWT_SECRET` | Chuỗi ngẫu nhiên 32 ký tự |
     | `JWT_REFRESH_SECRET` | Chuỗi ngẫu nhiên 32 ký tự |
     | `DATABASE_URL` | Connection string Neon/Supabase |
     | `ENVIRONMENT` | `production` |
     | `BACKEND_CORS_ORIGINS` | `https://<frontend-domain>` |
3. Chạy migration: `alembic upgrade head`.
4. Seed dữ liệu demo: `python seed.py` (tạo user `admin@demo.local` / `Admin123!`).
5. Cấu hình health check `/healthz`.
6. Cron hằng ngày: dùng Render Scheduler/Railway Cron chạy `python -m app.background.cron` hoặc gọi webhook `/api/v1/cron/daily` (khi mở rộng endpoint).

### 3. Frontend Next.js trên Vercel
1. Import repo, chọn thư mục `frontend`.
2. Environment: `NEXT_PUBLIC_API_BASE_URL=https://<backend-domain>/api/v1`.
3. Build command: `npm install && npm run build`; Output: `.next`.
4. Node 18.x (default Vercel) là đủ.

### 4. Upstash Redis (tùy chọn)
- Tạo DB free, lưu `UPSTASH_REDIS_REST_URL` & `UPSTASH_REDIS_REST_TOKEN` để dùng cho queue/cache sau này.

### 5. Tích hợp bên thứ ba (nhập từ UI)
- **GSC**: tạo OAuth Client (Desktop), lấy `client_id`, `client_secret`; tạo `refresh_token` bằng tool CLI (link trong UI); nhập tại `Cài đặt → Tích hợp`.
- **PSI**: tạo API key từ Google Cloud; nhập và bấm “Kiểm tra”.
- **WordPress**: bật Application Passwords, tạo user quyền Editor, nhập `site_url`, `username`, `application_password`.
- **IndexNow**: bấm “Sinh key”, tải file `.txt`, đặt tại root WP hoặc plugin. Dùng “Gửi thử URL”.
- **Gemini**: lấy API key từ Google AI Studio, nhập model (ví dụ `gemini-1.5-pro`) và giới hạn xuất bản/ngày. Khi tắt toggle, tính năng Content AI bị khoá.

## Chạy local

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export APP_SECRET=local-app-secret JWT_SECRET=jwt-secret JWT_REFRESH_SECRET=refresh-secret DATABASE_URL=postgresql://localhost/seo
alembic upgrade head
python seed.py
uvicorn app.main:app --reload --port 8000

# Frontend
cd ../frontend
npm install
npm run dev
```

- Frontend: `http://localhost:3000`
- Backend OpenAPI: `http://localhost:8000/api/v1/openapi.json` (Swagger UI tại `/docs`)
- Đăng nhập demo: `admin@demo.local / Admin123!`

## Cron & cảnh báo
- File `backend/app/background/cron.py` mô phỏng tác vụ daily ghi log.
- Tạo scheduler (Render/Railway hoặc GitHub Actions) chạy hằng ngày `python -m app.background.cron` hoặc gọi webhook khi được triển khai.

## Bảo mật & mã hoá
- Bảng `credentials.value_encrypted` lưu dữ liệu sau khi mã hoá AES-256-CFB với salt + IV ngẫu nhiên, key dẫn xuất từ `APP_SECRET`.
- UI luôn mask giá trị nhạy cảm (ví dụ `****abcd`).
- JWT access/refresh tách biệt, thời hạn mặc định 15 phút & 7 ngày.

## Lộ trình mở rộng
- Hoàn thiện Content AI (Gemini) với checklist E-E-A-T & kiểm duyệt thủ công.
- Thuật toán LinkScore (PageRank nội bộ + GSC + Similarity) và màn hình đồ thị Internal Link.
- Onpage checker (score 0–100), phát hiện cannibalization & content decay.
- RBAC đầy đủ, audit log UI, cảnh báo email.
- Tích hợp Upstash Redis cho queue và cache GSC/PSI.

## Kiểm thử
- Backend: `pytest`
- Frontend: `npm run lint` (ESLint có thể bổ sung sau)

## Tuân thủ & chính sách
- Không commit API key, `.env.sample` chỉ chứa biến trống.
- Dữ liệu lấy từ GSC/PSI chính thống, không scrape SERP.
- Content AI tôn trọng chính sách Gemini, có giới hạn xuất bản/ngày và bước duyệt thủ công.

---
**Tài khoản demo sau seed**
- Email: `admin@demo.local`
- Mật khẩu: `Admin123!`

> Repo sẵn sàng deploy free-tier (Vercel + Render/Railway + Neon/Supabase). Có migration, seed, cron mẫu, OpenAPI, UI tiếng Việt dark mode.
