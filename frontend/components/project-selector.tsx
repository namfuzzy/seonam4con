"use client";

import { useProjectStore } from "../store/project-store";

export function ProjectSelector() {
  const { projects, activeProjectId, setActiveProject } = useProjectStore();
  return (
    <select
      className="rounded-lg border border-slate-700 bg-slate-900 px-3 py-2 text-sm text-slate-100"
      value={activeProjectId ?? ""}
      onChange={(event) => setActiveProject(Number(event.target.value))}
    >
      {projects.map((project) => (
        <option key={project.id} value={project.id}>
          {project.name}
        </option>
      ))}
    </select>
  );
}
