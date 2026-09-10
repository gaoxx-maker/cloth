"use client";

import Link from "next/link";
import { useEffect, useState } from "react";

import { ProductFeed } from "@/components/ProductFeed";
import { getMyLikes } from "@/services/authApi";
import { removeLike } from "@/services/behaviorApi";
import { Product } from "@/types/product";

export default function AccountPage() {
  const [items, setItems] = useState<Product[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    getMyLikes().then(setItems).catch(() => setError("请先登录后查看喜欢的商品"));
  }, []);

  const unlike = async (product: Product) => {
    setItems((current) => current.filter((item) => item.id !== product.id));
    try {
      await removeLike(product.id);
    } catch {
      setItems((current) => [...current, product]);
    }
  };

  return (
    <section>
      <h1>我的喜欢</h1>
      {error ? <p>{error} <Link href="/login">去登录</Link></p> : (
        <ProductFeed
          items={items}
          hrefForProduct={(product) => `/product/${product.id}`}
          onUnlike={unlike}
          likedIds={new Set(items.map((item) => item.id))}
        />
      )}
    </section>
  );
}
