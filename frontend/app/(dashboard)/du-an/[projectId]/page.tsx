"use client";

import { useQuery } from "@tanstack/react-query";
import { useParams } from "next/navigation";

import { IntegrationCard } from "@/components/integration-card";
import { getIntegrations, getSites } from "@/lib/api";

function SiteIntegrations({ siteId }: { siteId: number }) {
  const { data, isLoading } = useQuery({
    queryKey: ["integrations", siteId],
    queryFn: () => getIntegrations(siteId)
  });

  if (isLoading) {
    return <p className="text-sm text-muted">Đang tải tích hợp...</p>;
  }

  if (!data || data.length === 0) {
    return <p className="text-sm text-muted">Chưa cấu hình tích hợp.</p>;
  }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {data.map((integration) => (
        <IntegrationCard key={integration.id} integration={integration} />
      ))}
    </div>
  );
}

export default function ProjectDetailPage() {
  const params = useParams<{ projectId: string }>();
  const projectId = Number(params.projectId);

  const { data, isLoading } = useQuery({
    queryKey: ["sites", projectId],
    queryFn: () => getSites(projectId),
    enabled: Number.isFinite(projectId)
  });

  return (
    <section className="space-y-6">
      <header className="space-y-2">
        <h1 className="text-2xl font-semibold">Chi tiết dự án #{projectId}</h1>
        <p className="text-sm text-muted">Danh sách site & tích hợp kết nối.</p>
      </header>

      {isLoading ? (
        <p className="text-sm text-muted">Đang tải site...</p>
      ) : !data || data.length === 0 ? (
        <p className="text-sm text-muted">Chưa có site nào cho dự án này.</p>
      ) : (
        <div className="space-y-8">
          {data.map((site) => (
            <div key={site.id} className="space-y-4">
              <div className="card">
                <h2 className="text-xl font-semibold">{site.domain}</h2>
                <p className="text-sm text-muted">WordPress: {site.wp_base_url ?? "Chưa thiết lập"}</p>
              </div>
              <SiteIntegrations siteId={site.id} />
            </div>
          ))}
        </div>
      )}
    </section>
  );
}
