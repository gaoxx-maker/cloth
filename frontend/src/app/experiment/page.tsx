"use client";

import { useEffect, useState } from "react";
import { api } from "@/services/api";
import { BackButton } from "@/components/BackButton";

interface ExperimentStats {
  events: Record<string, number>;
  like_rate: number | null;
  exploration_like_rate: number | null;
  products_per_session: number | null;
  unique_styles_per_session: number | null;
  replace_usage_rate: number | null;
  exploration_control_rate: number | null;
  replace_count: number;
  total_sessions: number;
  total_users: number;
}

const METRICS: { key: keyof ExperimentStats; label: string }[] = [
  { key: "like_rate", label: "喜欢率（likes / impressions）" },
  { key: "exploration_like_rate", label: "探索商品喜欢率（novelty > 0.6）" },
  { key: "products_per_session", label: "每次 Session 平均浏览商品数" },
  { key: "unique_styles_per_session", label: "每次 Session 平均风格跨度" },
  { key: "replace_usage_rate", label: "换一件使用率" },
  { key: "exploration_control_rate", label: "探索度调节率" },
];

function fmt(value: number | null): string {
  if (value === null || value === undefined) return "—";
  return Number.isInteger(value) ? String(value) : (value * 100).toFixed(1) + "%";
}

export default function ExperimentPage() {
  const [stats, setStats] = useState<ExperimentStats | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    api<ExperimentStats>("/experiments/stats").then(setStats).catch((e) => setError(String(e)));
  }, []);

  if (error) return <p>加载失败：{error}</p>;
  if (!stats) return <p>加载中…</p>;

  return (
    <>
      <BackButton />
      <h1>实验数据</h1>
      <article>
        <h2>核心指标</h2>
        <table>
          <tbody>
            {METRICS.map(({ key, label }) => (
              <tr key={key}>
                <td>{label}</td>
                <td>{fmt(stats[key] as number | null)}</td>
              </tr>
            ))}
          </tbody>
        </table>
        <p style={{ color: "#8a857c", fontSize: 13 }}>
          总会话 {stats.total_sessions} · 总匿名用户 {stats.total_users}
        </p>
      </article>
      <article>
        <h2>事件计数</h2>
        <pre>{JSON.stringify(stats.events, null, 2)}</pre>
      </article>
    </>
  );
}
