import { api } from "./api"; import { Product } from "@/types/product";
export const getProduct=(id:string)=>api<Product>(`/products/${id}`);
