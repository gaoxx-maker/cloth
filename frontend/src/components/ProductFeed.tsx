import { RecommendedProduct } from "@/types/recommendation"; import { ProductCard } from "./ProductCard";
export function ProductFeed({items}:{items:RecommendedProduct[]}) { return <section>{items.map(product=><ProductCard key={product.id} product={product}/>)}</section>; }
