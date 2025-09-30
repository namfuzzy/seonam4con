"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";

import { getProjects } from "@/lib/api";

export default function ProjectsPage() {
  const { data, isLoading } = useQuery({ queryKey: ["projects"], queryFn: getProjects });

  return (
    <section className="space-y-4">
      <header>
        <h1 className="text-2xl font-semibold">Quản lý dự án</h1>
        <p className="text-sm text-muted">Danh sách dự án và mục tiêu chính.</p>
      </header>
      {isLoading ? (
        <p className="text-sm text-muted">Đang tải...</p>
      ) : data && data.length > 0 ? (
        <ul className="space-y-3">
          {data.map((project) => (
            <li key={project.id} className="card flex items-center justify-between">
              <div>
                <p className="text-lg font-semibold">{project.name}</p>
                <p className="text-sm text-muted">{project.goals ?? "Chưa có mục tiêu"}</p>
              </div>
              <Link href={`/dashboard/du-an/${project.id}`} className="text-brand-500 hover:text-brand-400">
                Mở bảng dự án
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p className="text-sm text-muted">Chưa có dự án nào.</p>
      )}
    </section>
  );
}
