"use client";

import Link from "next/link";

import { useProjectStore } from "../../store/project-store";

export default function ProjectsPage() {
  const { projects, sites } = useProjectStore();
  return (
    <div className="space-y-6">
      <header className="card space-y-2">
        <h1 className="text-2xl font-semibold text-white">Danh sách dự án</h1>
        <p className="text-sm text-slate-400">Quản lý đa dự án, đa site WordPress.</p>
      </header>
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {projects.map((project) => {
          const projectSites = sites.filter((site) => site.projectId === project.id);
          return (
            <article key={project.id} className="card space-y-3">
              <div>
                <h2 className="text-lg font-semibold text-white">{project.name}</h2>
                <p className="text-sm text-slate-400">{project.goals}</p>
              </div>
              <div className="flex flex-wrap gap-2 text-xs text-slate-300">
                {projectSites.map((site) => (
                  <span key={site.id} className="badge">
                    {site.domain}
                  </span>
                ))}
              </div>
              <Link href={`/${project.id}/tich-hop`} className="text-sm text-emerald-300">
                Cấu hình tích hợp →
              </Link>
            </article>
          );
        })}
      </div>
    </div>
  );
}
