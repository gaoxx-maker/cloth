"use client";

import Link from "next/link";
import { use, useEffect, useState } from "react";
import { useRouter } from "next/navigation";

import { BackButton } from "@/components/BackButton";
import { getMyLikes } from "@/services/authApi";
import { recordBehavior, removeLike } from "@/services/behaviorApi";
import { getAccessToken, getSessionId } from "@/services/identity";
import { getProduct, getSimilarProducts } from "@/services/productApi";
import { Product, ProductDetail } from "@/types/product";

export default function ProductPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const [product, setProduct] = useState<ProductDetail>();
  const [similarProducts, setSimilarProducts] = useState<Product[]>([]);
  const [liked, setLiked] = useState(false);
  const router = useRouter();

  useEffect(() => {
    getProduct(id).then(setProduct).catch(console.error);
    getSimilarProducts(id).then(setSimilarProducts).catch(console.error);
    if (getAccessToken()) {
      getMyLikes()
        .then((products) => setLiked(products.some((item) => item.id === Number(id))))
        .catch(() => setLiked(false));
    } else {
      setLiked(false);
    }
  }, [id]);

  useEffect(() => {
    if (!getAccessToken()) return;
    const startedAt = performance.now();
    const sessionId = getSessionId();
    recordBehavior(Number(id), "open_detail", sessionId).catch(() => {});

    return () => {
      const durationSeconds = Math.round((performance.now() - startedAt) / 1000);
      if (durationSeconds >= 2) {
        recordBehavior(Number(id), "detail_dwell", sessionId, { duration_seconds: durationSeconds }).catch(() => {});
      }
    };
  }, [id]);

  const like = () => {
    if (!getAccessToken()) {
      router.push("/login");
      return;
    }
    if (liked) return;
    setLiked(true);
    recordBehavior(Number(id), "like", getSessionId(), { source: "product_detail" }).catch(() => setLiked(false));
  };

  const unlike = () => {
    if (!liked) return;
    setLiked(false);
    removeLike(Number(id)).catch(() => setLiked(true));
  };

  if (!product) return <p>加载中…</p>;

  return (
    <>
      <BackButton />
      <article className="product-detail">
        <h1>{product.title}</h1>
        <p className="detail-price">¥{product.price}</p>
        <p>{product.color} · {product.fit} · {product.category}</p>
        <p>{product.description}</p>
        <button className="like-button" onClick={liked ? unlike : like}>{liked ? "取消喜欢" : "♡ 喜欢"}</button>
      </article>
      <section className="offers">
        <h2>不同模拟商户报价</h2>
        {product.offers.map((offer) => (
          <Link className="offer" key={offer.id} href={offer.product_url || `/merchant/${offer.platform_code}/unknown`}>
            <span>{offer.platform}<small>模拟 {offer.platform_code.toUpperCase()} API</small></span>
            <strong>¥{offer.price}</strong>
          </Link>
        ))}
      </section>
      <section className="similar-products">
        <h2>相似商品</h2>
        {similarProducts.length ? similarProducts.map((item) => (
          <Link key={item.id} className="similar-product" href={`/product/${item.id}`}>
            <div
              className="similar-product__image"
              style={item.image_url ? { backgroundImage: `url(${item.image_url})` } : undefined}
              aria-hidden="true"
            />
            <span className="similar-product__title">{item.title}</span><strong>¥{item.price}</strong>
          </Link>
        )) : <p>暂未找到相似商品。</p>}
      </section>
    </>
  );
}
