import { api } from "./api";
import type { Product } from "@/types/product";
export type Account = { id: string; email: string; display_name: string; role: string; is_active: boolean };
export type AuthResponse = { access_token: string; token_type: string; expires_at: number; user: Account };
export const login = (email: string, password: string) => api<AuthResponse>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
export const register = (email: string, password: string, display_name: string) => api<AuthResponse>("/auth/register", { method: "POST", body: JSON.stringify({ email, password, display_name }) });
export const getMyLikes = () => api<Product[]>("/users/me/likes");
