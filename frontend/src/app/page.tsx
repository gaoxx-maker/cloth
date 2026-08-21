"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { ExplorationSlider } from "@/components/ExplorationSlider";
import { ProductFeed } from "@/components/ProductFeed";
import { SearchBar } from "@/components/SearchBar";
import { recordBehavior } from "@/services/behaviorApi";
import { getSessionId, getUserId } from "@/services/identity";
import { getFeed } from "@/services/recommendationApi";
import { RecommendedProduct } from "@/types/recommendation";

export default function Home() {
  const [items, setItems] = useState<RecommendedProduct[]>([]);
  const [level, setLevel] = useState(50);
  const [mode, setMode] = useState("balanced");
  const [userId, setUserId] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [refreshKey, setRefreshKey] = useState(0);
  const router = useRouter();

  useEffect(() => {
    setUserId(getUserId());
    setSessionId(getSessionId());
  }, []);

  useEffect(() => {
    if (!userId) return;
    getFeed(userId, level, mode, sessionId)
      .then((response) => {
        setItems(response.items);
      })
      .catch(console.error);
  }, [userId, sessionId, level, mode, refreshKey]);

  return (
    <>
      <h1>Fashion Explorer</h1>
      <p>符合审美，也留一点意外。<Link href="/experiment">查看实验数据</Link></p>
      <SearchBar />
      <ExplorationSlider value={level} onChange={setLevel} />
      <label>
        模式{" "}
        <select value={mode} onChange={(event) => setMode(event.target.value)}>
          <option value="baseline">传统</option>
          <option value="balanced">平衡</option>
          <option value="explore">探索</option>
        </select>
      </label>
      <div className="feed-toolbar"><p className="feed-hint">点击商品卡片查看详情 · 共 {items.length} 件</p><button onClick={() => setRefreshKey((key) => key + 1)}>换一批</button></div>
      <ProductFeed items={items} hrefForProduct={(product) => `/product/${product.id}`} />
    </>
  );
}
