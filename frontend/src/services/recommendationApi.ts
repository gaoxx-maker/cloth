import { api } from "./api";
import { FeedResponse, RecommendedProduct } from "@/types/recommendation";

export const getFeed = (
  userId: string,
  mode = "balanced",
  sessionId?: string,
) => {
  const params = new URLSearchParams({
    user_id: userId,
    mode,
  });
  if (sessionId) params.set("session_id", sessionId);
  return api<FeedResponse>(`/recommendations/feed?${params.toString()}`);
};

export const replaceProduct = (
  user_id: string,
  product_id: number,
  direction: string,
  exploration_level: number,
  sessionId?: string,
) =>
  api<RecommendedProduct>("/recommendations/replace", {
    method: "POST",
    body: JSON.stringify({ user_id, product_id, direction, exploration_level, session_id: sessionId }),
  });
