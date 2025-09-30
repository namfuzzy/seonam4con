"use client";

import { SimpleTable } from "../../../../../components/simple-table";
import { useProjectStore } from "../../../../../store/project-store";

const mockCwv = [
  { url: "/bai-viet-chu-luc", inp: "280ms", lcp: "2.1s", cls: "0.04", status: "Đạt" },
  { url: "/huong-dan", inp: "390ms", lcp: "2.6s", cls: "0.08", status: "Cần cải thiện" }
];

export default function ProjectOverview({ params }: { params: { projectId: string } }) {
  const projectId = Number(params.projectId);
  const { projects, sites } = useProjectStore();
  const project = projects.find((item) => item.id === projectId);
  const projectSites = sites.filter((site) => site.projectId === projectId);

  return (
    <div className="space-y-6">
      <section className="card space-y-2">
        <h1 className="text-2xl font-semibold text-white">{project?.name ?? "Dự án"}</h1>
        <p className="text-sm text-slate-400">Mục tiêu: {project?.goals ?? "Cập nhật mục tiêu trong Cài đặt"}</p>
        <div className="flex flex-wrap gap-2 text-sm text-slate-300">
          {projectSites.map((site) => (
            <span key={site.id} className="badge">
              {site.domain}
            </span>
          ))}
        </div>
      </section>

      <section className="card space-y-4">
        <header>
          <h2 className="text-lg font-semibold text-white">Core Web Vitals nổi bật</h2>
          <p className="text-sm text-slate-400">Từ PageSpeed Insights API</p>
        </header>
        <SimpleTable
          columns={[
            { key: "url", header: "URL" },
            { key: "inp", header: "INP" },
            { key: "lcp", header: "LCP" },
            { key: "cls", header: "CLS" },
            { key: "status", header: "Trạng thái" }
          ]}
          data={mockCwv}
        />
      </section>

      <section className="card space-y-3">
        <h3 className="text-lg font-semibold text-white">Nhật ký gần đây</h3>
        <ul className="space-y-2 text-sm text-slate-300">
          <li>• 09:00 - Cron daily đã kéo dữ liệu Search Console 28 ngày.</li>
          <li>• 08:45 - Admin nhập API key Gemini và giới hạn 3 bản nháp/ngày.</li>
          <li>• 08:10 - Hệ thống gợi ý 5 internal link mới cho cụm “chiến lược SEO”.</li>
        </ul>
      </section>
    </div>
  );
}
