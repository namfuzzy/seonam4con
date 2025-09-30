"use client";

import Link from "next/link";

import { useProjectStore } from "../../store/project-store";

export default function ProjectHome({ params }: { params: { projectId: string } }) {
  const { projects } = useProjectStore();
  const project = projects.find((item) => item.id === Number(params.projectId));

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-semibold text-white">{project?.name ?? "Dự án"}</h1>
      <p className="text-sm text-slate-400">Chọn tab bên dưới để quản lý.</p>
      <div className="flex flex-wrap gap-3">
        <Link href={`/${params.projectId}/tong-quan`} className="badge">
          Tổng quan dự án
        </Link>
        <Link href={`/${params.projectId}/tich-hop`} className="badge">
          Tích hợp API
        </Link>
      </div>
    </div>
  );
}
