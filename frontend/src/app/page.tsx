"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { ExplorationSlider } from "@/components/ExplorationSlider";
import { FeedbackButtons } from "@/components/FeedbackButtons";
import { ProductCard } from "@/components/ProductCard";
import { SearchBar } from "@/components/SearchBar";
import { recordBehavior } from "@/services/behaviorApi";
import { getSessionId, getUserId } from "@/services/identity";
import { getFeed, replaceProduct } from "@/services/recommendationApi";
import { RecommendedProduct } from "@/types/recommendation";

export default function Home() {
  const [items, setItems] = useState<RecommendedProduct[]>([]);
  const [level, setLevel] = useState(50);
  const [mode, setMode] = useState("balanced");
  const [userId, setUserId] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [refreshKey, setRefreshKey] = useState(0);

  // 匿名用户与 session：首次访问用 localStorage 生成并复用。
  useEffect(() => {
    setUserId(getUserId());
    setSessionId(getSessionId());
  }, []);

  useEffect(() => {
    if (!userId) return;
    getFeed(userId, level, mode, sessionId)
      .then((r) => setItems(r.items))
      .catch(console.error);
  }, [userId, sessionId, level, mode, refreshKey]);

  const current = items[0];

  const feedback = (event: string) => {
    if (!current) return;
    recordBehavior(userId, current.id, event, sessionId).finally(() =>
      setItems((x) => x.slice(1)),
    );
  };

  const replace = (direction: string) => {
    if (!current) return;
    replaceProduct(userId, current.id, direction, level, sessionId)
      .then((p) => setItems((x) => [p, ...x.slice(1)]))
      .catch(console.error);
  };

  return (
    <>
      <h1>Fashion Explorer</h1>
      <p>
        符合审美，也留一点意外。 <Link href="/experiment">查看实验数据</Link>
      </p>
      <SearchBar />
      <ExplorationSlider value={level} onChange={setLevel} />
      <label>
        模式{" "}
        <select value={mode} onChange={(e) => setMode(e.target.value)}>
          <option value="baseline">传统</option>
          <option value="balanced">平衡</option>
          <option value="explore">探索</option>
        </select>
      </label>

      {current ? (
        <>
          <p style={{ color: "#8a857c", fontSize: 13 }}>
            剩余 {items.length} 件 · 用户 {userId.slice(0, 8)}
          </p>
          <ProductCard product={current}>
            <FeedbackButtons onFeedback={feedback} onReplace={replace} />
          </ProductCard>
        </>
      ) : (
        <article>
          <p>这批推荐已浏览完。</p>
          <button onClick={() => setRefreshKey((k) => k + 1)}>再来一批</button>
        </article>
      )}
    </>
  );
}
