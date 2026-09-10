import { api } from "./api"; import { Product, ProductDetail } from "@/types/product";
export const getProduct=(id:string)=>api<ProductDetail>(`/products/${id}`);
export const getSimilarProducts=(id:string,limit=6)=>api<Product[]>(`/products/${id}/similar?limit=${limit}`);
export const getMerchantProduct=(platform:string,catalogId:string)=>api<Product>(`/products/merchant/${platform}/${catalogId}`);
