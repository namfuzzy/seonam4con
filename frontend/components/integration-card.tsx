import { BadgeCheck, PlugZap } from "lucide-react";

import { Integration } from "@/lib/api";

interface IntegrationCardProps {
  integration: Integration;
}

const integrationLabels: Record<string, string> = {
  GSC: "Google Search Console",
  PSI: "PageSpeed Insights",
  WP: "WordPress",
  INDEXNOW: "IndexNow",
  GEMINI: "Gemini AI"
};

export function IntegrationCard({ integration }: IntegrationCardProps) {
  const label = integrationLabels[integration.type] ?? integration.type;
  const credentials = integration.credentials ?? [];
  return (
    <div className="card space-y-3">
      <div className="flex items-center justify-between">
        <div className="flex items-center gap-2">
          <PlugZap className="h-5 w-5 text-brand-500" />
          <h3 className="text-lg font-semibold">{label}</h3>
        </div>
        {integration.enabled ? (
          <span className="flex items-center gap-1 text-sm text-emerald-400">
            <BadgeCheck className="h-4 w-4" /> Đang bật
          </span>
        ) : (
          <span className="text-sm text-muted">Đang tắt</span>
        )}
      </div>
      <div className="rounded-lg border border-slate-800 bg-slate-900/40 p-3 text-xs text-muted">
        {credentials.length === 0 ? (
          <p>Chưa có khoá nào.</p>
        ) : (
          <ul className="space-y-2">
            {credentials.map((credential) => (
              <li key={credential.id} className="flex items-center justify-between">
                <span>{credential.key_name}</span>
                <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] uppercase">Đã mã hoá</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
