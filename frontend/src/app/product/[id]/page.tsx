"use client";

import Link from "next/link";
import { use, useEffect, useState } from "react";

import { recordBehavior } from "@/services/behaviorApi";
import { getSessionId, getUserId } from "@/services/identity";
import { getProduct } from "@/services/productApi";
import { Product } from "@/types/product";

export default function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [product, setProduct] = useState<Product>();

  useEffect(() => {
    getProduct(id).then(setProduct).catch(console.error);
  }, [id]);

  // 打开详情即记录 open_detail 行为，作为兴趣信号（权重 +1）。
  useEffect(() => {
    recordBehavior(getUserId(), Number(id), "open_detail", getSessionId()).catch(() => {});
  }, [id]);

  if (!product) return <p>加载中…</p>;

  return (
    <article>
      <h1>{product.title}</h1>
      <p>
        {product.brand} · ¥{product.price}
      </p>
      <p>{product.style_tags.join(" · ")}</p>
      <p>
        {product.color} / {product.fit} / {product.category}
      </p>
      <p>{product.description}</p>
      <p>
        <Link href="/">← 返回推荐</Link>
      </p>
    </article>
  );
}
