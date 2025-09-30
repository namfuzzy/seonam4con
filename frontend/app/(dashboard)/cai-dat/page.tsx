"use client";

import { useQuery } from "@tanstack/react-query";

import { IntegrationCard } from "@/components/integration-card";
import { ProjectSelector } from "@/components/project-selector";
import { getIntegrations, getProjects, getSites } from "@/lib/api";
import { useProjectStore } from "@/store/project-store";

export default function SettingsPage() {
  const { selectedProjectId } = useProjectStore();
  const { data: projects } = useQuery({ queryKey: ["projects"], queryFn: getProjects });
  const projectId = selectedProjectId ?? projects?.[0]?.id;

  const { data: sites } = useQuery({
    queryKey: ["sites", projectId],
    queryFn: () => getSites(projectId ?? 0),
    enabled: Boolean(projectId)
  });

  const firstSite = sites?.[0];

  const { data: integrations } = useQuery({
    queryKey: ["integrations", firstSite?.id],
    queryFn: () => getIntegrations(firstSite?.id ?? 0),
    enabled: Boolean(firstSite?.id)
  });

  return (
    <section className="space-y-6">
      <header className="space-y-2">
        <h1 className="text-2xl font-semibold">Cài đặt & tích hợp</h1>
        <p className="text-sm text-muted">
          Nhập API key cho Google Search Console, PageSpeed Insights, WordPress, IndexNow, Gemini. Tất cả khoá sẽ được mã hoá bằng APP_SECRET.
        </p>
      </header>

      <div className="card space-y-3">
        <h2 className="text-lg font-semibold">Chọn dự án & site</h2>
        <ProjectSelector />
        {firstSite ? (
          <p className="text-sm text-muted">Đang xem tích hợp của site {firstSite.domain}.</p>
        ) : (
          <p className="text-sm text-muted">Hãy thêm site cho dự án để cấu hình tích hợp.</p>
        )}
      </div>

      {firstSite && integrations ? (
        <div className="grid gap-4 md:grid-cols-2">
          {integrations.map((integration) => (
            <IntegrationCard key={integration.id} integration={integration} />
          ))}
        </div>
      ) : (
        <p className="text-sm text-muted">Không tìm thấy tích hợp.</p>
      )}
    </section>
  );
}
