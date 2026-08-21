export interface Product { id:number; title:string; description:string; brand:string; category:string; price:number; color:string; fit:string; style_primary:string; style_secondary?:string; style_tags:string[]; novelty_score:number; quality_score:number; image_url?:string; product_url?:string }
export interface ProductOffer { id:number; platform:string; platform_code:string; price:number; original_price?:number; product_url?:string }
export interface ProductDetail extends Product { offers:ProductOffer[] }
