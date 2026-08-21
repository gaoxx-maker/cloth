import { api } from "./api"; import { Product, ProductDetail } from "@/types/product";
export const getProduct=(id:string)=>api<ProductDetail>(`/products/${id}`);
export const getMerchantProduct=(platform:string,catalogId:string)=>api<Product>(`/products/merchant/${platform}/${catalogId}`);
