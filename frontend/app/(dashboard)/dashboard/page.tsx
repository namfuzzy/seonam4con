"use client";

import { useMemo } from "react";

import { KpiCard } from "../../../components/kpi-card";
import { SimpleTable } from "../../../components/simple-table";
import { useProjectStore } from "../../../store/project-store";

const mockPages = [
  { url: "https://demo-site.vn/bai-viet-chu-luc", clicks: 1320, impressions: 5400, ctr: "24.4%", position: "5.2" },
  { url: "https://demo-site.vn/huong-dan", clicks: 820, impressions: 3800, ctr: "21.6%", position: "7.4" }
];

const mockQueries = [
  { query: "chiến lược seo b2b", clicks: 320, impressions: 1200, change: "+18%" },
  { query: "core web vitals là gì", clicks: 210, impressions: 980, change: "+9%" }
];

export default function DashboardPage() {
  const { projects, activeProjectId } = useProjectStore();
  const project = useMemo(() => projects.find((item) => item.id === activeProjectId), [projects, activeProjectId]);

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <KpiCard title="Clicks 28 ngày" value="12.540" delta="▲ 14% so với 28 ngày trước" />
        <KpiCard title="Impressions" value="86.210" delta="▲ 8%" />
        <KpiCard title="CTR trung bình" value="14,6%" delta="+0,9 điểm" />
        <KpiCard title="Vị trí TB" value="7,4" delta="▼ 0,3" />
      </div>

      <section className="card space-y-4">
        <header>
          <h2 className="text-xl font-semibold text-white">Diễn biến dự án: {project?.name}</h2>
          <p className="text-sm text-slate-400">So sánh 7 / 28 / 90 ngày, phát hiện biến động chính.</p>
        </header>
        <div className="grid gap-4 md:grid-cols-2">
          <div>
            <h3 className="mb-2 text-sm font-semibold text-slate-300">Trang tăng trưởng</h3>
            <SimpleTable
              columns={[
                { key: "url", header: "URL" },
                { key: "clicks", header: "Clicks" },
                { key: "ctr", header: "CTR" }
              ]}
              data={mockPages}
            />
          </div>
          <div>
            <h3 className="mb-2 text-sm font-semibold text-slate-300">Truy vấn nổi bật</h3>
            <SimpleTable
              columns={[
                { key: "query", header: "Truy vấn" },
                { key: "clicks", header: "Clicks" },
                { key: "change", header: "Biến động" }
              ]}
              data={mockQueries}
            />
          </div>
        </div>
      </section>

      <section className="card space-y-4">
        <header className="flex items-center justify-between">
          <div>
            <h3 className="text-lg font-semibold text-white">Cảnh báo kỹ thuật & CWV</h3>
            <p className="text-sm text-slate-400">Ưu tiên xử lý theo Impact × Effort</p>
          </div>
          <span className="badge">3 cảnh báo mới</span>
        </header>
        <ul className="space-y-3 text-sm text-slate-200">
          <li>• 4 URL có INP &gt; 400ms cần tối ưu tương tác.</li>
          <li>• Sitemap thiếu cập nhật URL mới trong 3 ngày gần nhất.</li>
          <li>• 2 URL trả về 404 từ internal link quan trọng.</li>
        </ul>
      </section>
    </div>
  );
}
