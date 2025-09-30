interface KPIProps {
  title: string;
  value: string;
  change?: string;
}

export function KPICard({ title, value, change }: KPIProps) {
  return (
    <div className="card">
      <p className="text-sm text-muted">{title}</p>
      <p className="mt-2 text-3xl font-semibold">{value}</p>
      {change ? <p className="mt-1 text-xs text-emerald-400">{change}</p> : null}
    </div>
  );
}
