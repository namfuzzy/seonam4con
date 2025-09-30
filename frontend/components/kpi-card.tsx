interface KpiCardProps {
  title: string;
  value: string;
  delta?: string;
}

export function KpiCard({ title, value, delta }: KpiCardProps) {
  return (
    <div className="card space-y-2">
      <div className="text-sm uppercase tracking-wide text-slate-400">{title}</div>
      <div className="text-3xl font-semibold text-white">{value}</div>
      {delta && <div className="badge">{delta}</div>}
    </div>
  );
}
