"use client";

import { useEffect, useState } from "react";

import { BackButton } from "@/components/BackButton";
import { ProductFeed } from "@/components/ProductFeed";
import { api } from "@/services/api";
import { Product } from "@/types/product";

export default function SearchPage() {
  const [items, setItems] = useState<Product[]>([]);
  useEffect(() => {
    const query = new URLSearchParams(location.search).get("q");
    if (query) api<Product[]>(`/search?q=${encodeURIComponent(query)}`).then(setItems).catch(console.error);
  }, []);
  return <><BackButton /><h1>搜索结果</h1><p className="feed-hint">点击商品卡片查看不同模拟商户的报价</p><ProductFeed items={items} hrefForProduct={(product) => `/product/${product.id}`} /></>;
}
