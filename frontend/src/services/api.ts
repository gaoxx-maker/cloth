import { API_URL } from "@/config/constants";

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...init,
  });
  if (!response.ok) {
    throw new Error(await response.text());
  }
  const text = await response.text();
  return (text ? JSON.parse(text) : undefined) as T;
}
