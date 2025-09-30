"use client";

import { create } from "zustand";

interface ProjectState {
  selectedProjectId: number | null;
  setProject: (id: number) => void;
}

export const useProjectStore = create<ProjectState>((set) => ({
  selectedProjectId: null,
  setProject: (id) => set({ selectedProjectId: id })
}));
