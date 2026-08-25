"use client";

export function getOrCreateId(key: string): string {
  let id = localStorage.getItem(key);
  if (!id) {
    id =
      typeof crypto !== "undefined" && "randomUUID" in crypto
        ? crypto.randomUUID()
        : `${Date.now()}-${Math.random().toString(36).slice(2)}`;
    localStorage.setItem(key, id);
  }
  return id;
}

export const getUserId = () => getOrCreateId("fashion-user-id");
export const getSessionId = () => getOrCreateId("fashion-session-id");
export const getAccessToken = () => typeof window === "undefined" ? null : localStorage.getItem("fashion-access-token");
export const setAccessToken = (token: string) => localStorage.setItem("fashion-access-token", token);
export const clearAccessToken = () => localStorage.removeItem("fashion-access-token");
