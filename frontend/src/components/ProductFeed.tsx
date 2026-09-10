import { Product } from "@/types/product";
import { RecommendedProduct } from "@/types/recommendation";

import { ProductCard } from "./ProductCard";

type FeedProduct = Product | RecommendedProduct;

export function ProductFeed<T extends FeedProduct>({
  items,
  onLike,
  onUnlike,
  hrefForProduct,
  likedIds = new Set<number>(),
}: {
  items: T[];
  onLike?: (product: T) => void;
  onUnlike?: (product: T) => void;
  hrefForProduct?: (product: T) => string;
  likedIds?: Set<number>;
}) {
  return (
    <section className="product-grid" aria-label="商品列表">
      {items.map((product) => (
        <ProductCard key={product.id} product={product} onLike={onLike} onUnlike={onUnlike} href={hrefForProduct?.(product)} liked={likedIds.has(product.id)} />
      ))}
    </section>
  );
}
