"use client";

import { useQuery } from "@tanstack/react-query";
import Link from "next/link";
import { useEffect } from "react";

import { getProjects } from "@/lib/api";
import { useProjectStore } from "@/store/project-store";

export function ProjectSelector() {
  const { data } = useQuery({ queryKey: ["projects"], queryFn: getProjects });
  const { selectedProjectId, setProject } = useProjectStore();

  useEffect(() => {
    if (!selectedProjectId && data && data.length > 0) {
      setProject(data[0].id);
    }
  }, [data, selectedProjectId, setProject]);

  if (!data || data.length === 0) {
    return <span className="text-sm text-muted">Chưa có dự án</span>;
  }

  const active = data.find((item) => item.id === selectedProjectId) ?? data[0];

  return (
    <div className="flex items-center gap-2 text-sm">
      <span className="text-muted">Dự án:</span>
      <select
        className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-1"
        value={active?.id}
        onChange={(event) => setProject(Number(event.target.value))}
      >
        {data.map((project) => (
          <option key={project.id} value={project.id}>
            {project.name}
          </option>
        ))}
      </select>
      <Link href={`/dashboard/du-an/${active?.id}`} className="text-brand-500 hover:text-brand-400">
        Chi tiết
      </Link>
    </div>
  );
}
