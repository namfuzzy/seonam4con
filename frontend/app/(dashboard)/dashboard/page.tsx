"use client";

import { useQuery } from "@tanstack/react-query";

import { KPICard } from "@/components/kpi-card";
import { SimpleTable } from "@/components/simple-table";
import { getProjects } from "@/lib/api";

const columns = [
  {
    header: "Tên dự án",
    accessor: (item: { name: string; goals?: string | null }) => item.name
  },
  {
    header: "Mục tiêu",
    accessor: (item: { goals?: string | null }) => item.goals ?? "—"
  }
];

export default function DashboardPage() {
  const { data, isLoading } = useQuery({ queryKey: ["projects"], queryFn: getProjects });

  return (
    <div className="space-y-6">
      <section className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <KPICard title="Clicks 28 ngày" value="12.540" change="▲ +6.2%" />
        <KPICard title="Impressions 28 ngày" value="187.200" change="▲ +4.1%" />
        <KPICard title="CTR trung bình" value="6,7%" change="▲ +0,3 điểm" />
        <KPICard title="Vị trí trung bình" value="5,2" change="▼ -0,4" />
      </section>

      <section className="space-y-3">
        <div>
          <h2 className="text-xl font-semibold">Dự án đang theo dõi</h2>
          <p className="text-sm text-muted">Danh sách dự án bạn sở hữu trong hệ thống.</p>
        </div>
        {isLoading ? <p className="text-sm text-muted">Đang tải...</p> : <SimpleTable data={data ?? []} columns={columns} emptyText="Chưa có dự án nào" />}
      </section>
    </div>
  );
}
