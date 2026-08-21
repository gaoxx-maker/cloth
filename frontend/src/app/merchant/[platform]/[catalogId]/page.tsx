"use client";

import { use, useEffect, useState } from "react";

import { BackButton } from "@/components/BackButton";
import { getMerchantProduct } from "@/services/productApi";
import { Product } from "@/types/product";

export default function MerchantPage({ params }: { params: Promise<{ platform: string; catalogId: string }> }) {
  const { platform, catalogId } = use(params);
  const [product, setProduct] = useState<Product>();
  useEffect(() => { getMerchantProduct(platform, catalogId).then(setProduct).catch(console.error); }, [platform, catalogId]);
  if (!product) return <p>加载中…</p>;
  return <><BackButton fallback={`/product/${product.id}`} /><article className="merchant-page"><p className="merchant-eyebrow">{platform.toUpperCase()} 模拟商户页面</p><h1>{product.title}</h1><p className="detail-price">¥{product.price}</p><p>{product.description}</p><p>该页面用于模拟外部商户 API 的落地页和报价跳转。</p></article></>;
}
