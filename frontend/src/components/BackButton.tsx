"use client";

import { useRouter } from "next/navigation";

export function BackButton({ fallback = "/" }: { fallback?: string }) {
  const router = useRouter();
  return <button className="back-button" onClick={() => window.history.length > 1 ? router.back() : router.push(fallback)}>← 返回</button>;
}
