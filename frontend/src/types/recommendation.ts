import { Product } from "./product";
export interface RecommendedProduct extends Product { recommendation:{score:number;interest_score:number;novelty_score:number;reason:string[]} }
export interface FeedResponse { items:RecommendedProduct[]; meta:{exploration_level:number;algorithm:string;mode:string;season:string} }
