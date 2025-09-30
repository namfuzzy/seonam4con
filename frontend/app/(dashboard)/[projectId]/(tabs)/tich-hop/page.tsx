import Link from "next/link";

import { IntegrationCard } from "../../../../../components/integration-card";

const gscFields = [
  { name: "client_id", label: "Client ID" },
  { name: "client_secret", label: "Client Secret" },
  { name: "refresh_token", label: "Refresh Token" }
];

const psiFields = [{ name: "api_key", label: "API Key" }];

const wordpressFields = [
  { name: "site_url", label: "URL WordPress", type: "text", placeholder: "https://example.com" },
  { name: "username", label: "Username", type: "text" },
  { name: "application_password", label: "Application Password" }
];

const geminiFields = [
  { name: "api_key", label: "Gemini API Key" },
  { name: "model", label: "Model", type: "text", placeholder: "gemini-1.5-pro" },
  { name: "daily_limit", label: "Giới hạn xuất bản/ngày", type: "number" }
];

export default function IntegrationPage() {
  return (
    <div className="space-y-6">
      <header className="card space-y-2">
        <h1 className="text-2xl font-semibold text-white">Cài đặt & tích hợp</h1>
        <p className="text-sm text-slate-400">
          Nhập khóa API, bật/tắt từng dịch vụ. Tất cả thông tin được mã hoá AES-256 bằng khóa <code>APP_SECRET</code>.
        </p>
        <Link href="/huong-dan" className="text-sm text-emerald-300">
          Xem hướng dẫn cấu hình chi tiết →
        </Link>
      </header>

      <IntegrationCard title="Google Search Console" description="Đồng bộ Search Analytics theo site" fields={gscFields} />
      <IntegrationCard title="PageSpeed Insights" description="Theo dõi Core Web Vitals & Lighthouse" fields={psiFields} />
      <IntegrationCard title="WordPress" description="Đăng nháp, media, taxonomy" fields={wordpressFields} />
      <IntegrationCard title="IndexNow" description="Sinh key & gửi URL" fields={[{ name: "key", label: "IndexNow Key" }]} />
      <IntegrationCard title="Gemini AI" description="Sinh brief/outline/draft, giới hạn xuất bản" fields={geminiFields} />
    </div>
  );
}
