import { api } from "./api";

export const recordBehavior = (
  user_id: string,
  product_id: number,
  event_type: string,
  session_id?: string,
  metadata?: Record<string, unknown>,
) =>
  api<{ ok: boolean }>("/behaviors", {
    method: "POST",
    body: JSON.stringify({ user_id, product_id, event_type, session_id, metadata }),
  });
