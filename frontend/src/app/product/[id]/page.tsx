"use client";

import Link from "next/link";
import { use, useEffect, useState } from "react";

import { BackButton } from "@/components/BackButton";
import { recordBehavior } from "@/services/behaviorApi";
import { getSessionId, getUserId } from "@/services/identity";
import { getProduct } from "@/services/productApi";
import { ProductDetail } from "@/types/product";

export default function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [product, setProduct] = useState<ProductDetail>();
  const [liked, setLiked] = useState(false);
  useEffect(() => { getProduct(id).then(setProduct).catch(console.error); }, [id]);
  useEffect(() => { recordBehavior(getUserId(), Number(id), "open_detail", getSessionId()).catch(() => {}); }, [id]);
  const like = () => {
    if (liked) return;
    setLiked(true);
    recordBehavior(getUserId(), Number(id), "like", getSessionId(), { source: "product_detail" }).catch(() => setLiked(false));
  };
  if (!product) return <p>加载中…</p>;
  return <><BackButton /><article className="product-detail"><h1>{product.title}</h1><p className="detail-price">¥{product.price}</p><p>{product.color} · {product.fit} · {product.category}</p><p>{product.description}</p><button className="like-button" onClick={like} disabled={liked}>{liked ? "已喜欢" : "♡ 喜欢"}</button></article><section className="offers"><h2>不同模拟商户报价</h2>{product.offers.map((offer) => <Link className="offer" key={offer.id} href={offer.product_url || `/merchant/${offer.platform_code}/unknown`}><span>{offer.platform}<small>模拟 {offer.platform_code.toUpperCase()} API</small></span><strong>¥{offer.price}</strong></Link>)}</section></>;
}
