import axios from "axios";

export const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000/api/v1",
  withCredentials: false
});

export async function fetcher<T>(url: string): Promise<T> {
  const response = await apiClient.get<T>(url);
  return response.data;
}
