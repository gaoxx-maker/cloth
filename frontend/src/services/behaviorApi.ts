import { api } from "./api";

export const recordBehavior = (
  product_id: number,
  event_type: string,
  session_id?: string,
  metadata?: Record<string, unknown>,
) =>
  api<{ ok: boolean }>("/behaviors", {
    method: "POST",
    body: JSON.stringify({ product_id, event_type, session_id, metadata }),
  });

export const removeLike = (productId: number) =>
  api<{ ok: boolean }>(`/behaviors/likes/${productId}`, { method: "DELETE" });
