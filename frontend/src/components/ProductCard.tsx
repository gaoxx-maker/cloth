"use client";

import type { KeyboardEvent, MouseEvent } from "react";
import { useRouter } from "next/navigation";

import { Product } from "@/types/product";
import { RecommendedProduct } from "@/types/recommendation";

type CardProduct = Product | RecommendedProduct;

function hasRecommendation(product: CardProduct): product is RecommendedProduct {
  return "recommendation" in product;
}

export function ProductCard<T extends CardProduct>({
  product,
  onLike,
  onUnlike,
  href,
  liked = false,
}: {
  product: T;
  onLike?: (product: T) => void;
  onUnlike?: (product: T) => void;
  href?: string;
  liked?: boolean;
}) {
  const router = useRouter();
  const activate = () => href ? router.push(href) : onLike?.(product);
  const activateFromKeyboard = (event: KeyboardEvent<HTMLElement>) => {
    if (event.key === "Enter" || event.key === " ") {
      event.preventDefault();
      activate();
    }
  };
  const likeFromPreview = (event: MouseEvent<HTMLButtonElement>) => {
    event.stopPropagation();
    if (liked) onUnlike?.(product);
    else onLike?.(product);
  };

  return (
    <article
      className={`product-card${onLike || href ? " product-card--clickable" : ""}${liked ? " product-card--liked" : ""}`}
      onClick={activate}
      onKeyDown={activateFromKeyboard}
      role={href ? "link" : onLike ? "button" : undefined}
      tabIndex={onLike || href ? 0 : undefined}
      aria-label={href ? `查看 ${product.title} 的详情` : onLike ? `喜欢 ${product.title}` : undefined}
    >
      <div className="product-pattern" style={product.image_url ? { backgroundImage: `url(${product.image_url})` } : undefined}>
        {!product.image_url && <span className="product-pattern__swatch" aria-hidden="true" />}
        <p className="product-pattern__description">{product.description}</p>
      </div>
      <div className="product-card__body">
        <div className="product-card__heading">
          <h2>{product.title}</h2>
          {liked && <span className="product-card__liked">已喜欢</span>}
        </div>
        <p className="product-card__meta">{product.brand} · {product.category}</p>
        <p className="product-card__price">¥{product.price}</p>
        <p className="product-card__tags">{product.style_tags.join(" · ")}</p>
        {hasRecommendation(product) && (
          <p className="product-card__reason">推荐理由：{product.recommendation.reason.join("、")}</p>
        )}
        {(onLike || onUnlike) && (
          <button
            className="product-card__like-button"
            type="button"
            onClick={likeFromPreview}
            onKeyDown={(event) => event.stopPropagation()}
            disabled={liked ? !onUnlike : !onLike}
            aria-label={`${liked ? "取消喜欢" : "喜欢"} ${product.title}`}
          >
            {liked ? "取消喜欢" : "♡ 喜欢"}
          </button>
        )}
      </div>
    </article>
  );
}
