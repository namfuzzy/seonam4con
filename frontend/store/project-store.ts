"use client";

import { create } from "zustand";

export type Project = {
  id: number;
  name: string;
  goals?: string;
  kpi?: string;
};

export type Site = {
  id: number;
  domain: string;
  projectId: number;
};

interface ProjectState {
  projects: Project[];
  sites: Site[];
  activeProjectId: number | null;
  setProjects: (projects: Project[]) => void;
  setSites: (sites: Site[]) => void;
  setActiveProject: (projectId: number) => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  projects: [
    { id: 1, name: "Dự án Demo", goals: "Tăng trưởng Click 20%" },
    { id: 2, name: "Website Sản phẩm", goals: "Ổn định CTR" }
  ],
  sites: [
    { id: 1, domain: "demo-site.vn", projectId: 1 },
    { id: 2, domain: "blog.demo-site.vn", projectId: 1 },
    { id: 3, domain: "product.vn", projectId: 2 }
  ],
  activeProjectId: 1,
  setProjects: (projects) => set({ projects }),
  setSites: (sites) => set({ sites }),
  setActiveProject: (projectId) => set({ activeProjectId: projectId })
}));
