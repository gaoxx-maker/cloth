"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { ProductFeed } from "@/components/ProductFeed";
import { SearchBar } from "@/components/SearchBar";
import { getMyLikes } from "@/services/authApi";
import { recordBehavior, removeLike } from "@/services/behaviorApi";
import { getAccessToken, getSessionId, getUserId } from "@/services/identity";
import { getFeed } from "@/services/recommendationApi";
import { RecommendedProduct } from "@/types/recommendation";

type FeedBatch = {
  items: RecommendedProduct[];
  season: string;
};

export default function Home() {
  const [batches, setBatches] = useState<FeedBatch[]>([]);
  const [activeBatch, setActiveBatch] = useState(0);
  const [mode, setMode] = useState("balanced");
  const [userId, setUserId] = useState("");
  const [sessionId, setSessionId] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [likedIds, setLikedIds] = useState<Set<number>>(new Set());
  const router = useRouter();

  useEffect(() => {
    setUserId(getUserId());
    setSessionId(getSessionId());
    if (getAccessToken()) {
      getMyLikes()
        .then((products) => setLikedIds(new Set(products.map((product) => product.id))))
        .catch(() => setLikedIds(new Set()));
    }
  }, []);

  useEffect(() => {
    if (!userId) return;
    setIsLoading(true);
    // 批次只存在当前页面组件的内存里；重新打开首页时会自然重置。
    setBatches([]);
    setActiveBatch(0);
    getFeed(userId, mode, sessionId)
      .then((response) => {
        setBatches([{ items: response.items, season: response.meta.season }]);
      })
      .catch(console.error)
      .finally(() => setIsLoading(false));
  }, [userId, sessionId, mode]);

  const loadNextBatch = () => {
    if (!userId || isLoading) return;
    setIsLoading(true);
    getFeed(userId, mode, sessionId)
      .then((response) => {
        setBatches((current) => [...current, { items: response.items, season: response.meta.season }]);
        setActiveBatch(batches.length);
      })
      .catch(console.error)
      .finally(() => setIsLoading(false));
  };

  const visibleBatch = batches[activeBatch];

  const likeFromPreview = async (product: RecommendedProduct) => {
    if (!getAccessToken()) {
      router.push("/login");
      return;
    }
    if (likedIds.has(product.id)) return;
    setLikedIds((current) => new Set(current).add(product.id));
    try {
      await recordBehavior(product.id, "like", sessionId, { source: "product_preview" });
    } catch {
      setLikedIds((current) => {
        const next = new Set(current);
        next.delete(product.id);
        return next;
      });
    }
  };

  const unlikeFromPreview = async (product: RecommendedProduct) => {
    if (!likedIds.has(product.id)) return;
    setLikedIds((current) => {
      const next = new Set(current);
      next.delete(product.id);
      return next;
    });
    try {
      await removeLike(product.id);
    } catch {
      setLikedIds((current) => new Set(current).add(product.id));
    }
  };

  return (
    <>
      <h1>Fashion Explorer</h1>
      <p>符合审美，也留一点意外。<Link href="/experiment">查看实验数据</Link></p>
      <SearchBar />
      <div className="mode-picker" role="group" aria-label="推荐模式">
        {[
          ["balanced", "平衡", "兼顾熟悉感与新发现"],
          ["traditional", "传统", "更贴近已形成的偏好"],
          ["explore", "探索", "发现更多不同风格"],
        ].map(([value, label, description]) => (
          <button
            key={value}
            className={`mode-option${mode === value ? " mode-option--active" : ""}`}
            onClick={() => setMode(value)}
            aria-pressed={mode === value}
          >
            <strong>{label}</strong><span>{description}</span>
          </button>
        ))}
      </div>
      <div className="feed-toolbar">
        <p className="feed-hint">{visibleBatch?.season ? `${visibleBatch.season} 当季推荐 · ` : ""}点击商品卡片查看详情 · 共 {visibleBatch?.items.length ?? 0} 件</p>
        <button onClick={loadNextBatch} disabled={isLoading}>{isLoading ? "加载中…" : "换一批"}</button>
      </div>
      <ProductFeed
        items={visibleBatch?.items ?? []}
        hrefForProduct={(product) => `/product/${product.id}`}
        onLike={likeFromPreview}
        onUnlike={unlikeFromPreview}
        likedIds={likedIds}
      />
      {batches.length > 0 && (
        <nav className="feed-pagination" aria-label="商品批次翻页">
          <button onClick={() => setActiveBatch((page) => page - 1)} disabled={activeBatch === 0}>上一批</button>
          <div className="feed-pagination__pages">
            {batches.map((_, index) => (
              <button
                key={index}
                className={index === activeBatch ? "feed-pagination__page--active" : ""}
                onClick={() => setActiveBatch(index)}
                aria-label={`查看第 ${index + 1} 批商品`}
                aria-current={index === activeBatch ? "page" : undefined}
              >
                {index + 1}
              </button>
            ))}
          </div>
          <button onClick={loadNextBatch} disabled={isLoading}>{isLoading ? "加载中…" : "下一批"}</button>
        </nav>
      )}
    </>
  );
}
