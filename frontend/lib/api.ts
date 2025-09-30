import axios from "axios";

export interface Project {
  id: number;
  name: string;
  goals?: string | null;
  created_at?: string;
}

export interface Site {
  id: number;
  domain: string;
  wp_base_url?: string | null;
  project_id?: number;
}

export interface IntegrationCredential {
  id: number;
  key_name: string;
  created_at?: string;
}

export interface Integration {
  id: number;
  type: string;
  enabled: boolean;
  credentials?: IntegrationCredential[];
}

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000/api/v1"
});

export async function getProjects(): Promise<Project[]> {
  const token = process.env.NEXT_PUBLIC_DEMO_TOKEN;
  try {
    const response = await api.get("/projects/", {
      headers: token ? { Authorization: `Bearer ${token}` } : undefined
    });
    return response.data;
  } catch (error) {
    console.warn("Không thể tải dự án", error);
    return [];
  }
}

export async function getSites(projectId: number): Promise<Site[]> {
  const token = process.env.NEXT_PUBLIC_DEMO_TOKEN;
  if (!projectId) {
    return [];
  }
  try {
    const response = await api.get("/sites/", {
      params: { project_id: projectId },
      headers: token ? { Authorization: `Bearer ${token}` } : undefined
    });
    return response.data;
  } catch (error) {
    console.warn("Không thể tải site", error);
    return [];
  }
}

export async function getIntegrations(siteId: number): Promise<Integration[]> {
  const token = process.env.NEXT_PUBLIC_DEMO_TOKEN;
  if (!siteId) {
    return [];
  }
  try {
    const response = await api.get("/integrations/", {
      params: { site_id: siteId },
      headers: token ? { Authorization: `Bearer ${token}` } : undefined
    });
    return response.data;
  } catch (error) {
    console.warn("Không thể tải tích hợp", error);
    return [];
  }
}
