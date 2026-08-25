from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.product import ProductDetailRead, ProductRead
from app.services.product_service import ProductService
router=APIRouter(prefix="/products",tags=["products"])
@router.get("",response_model=list[ProductRead])
def list_products(limit:int=20,offset:int=0,db:Session=Depends(get_db)): return ProductService(db).list_products(limit,offset)
@router.get("/merchant/{platform_code}/{catalog_id}",response_model=ProductRead)
def get_merchant_product(platform_code:str,catalog_id:str,db:Session=Depends(get_db)):
    product=ProductService(db).get_merchant_product(platform_code,catalog_id)
    if not product: raise HTTPException(404,"Merchant product not found")
    return product
@router.get("/{product_id}/similar",response_model=list[ProductRead])
def get_similar_products(product_id:int,limit:int=6,db:Session=Depends(get_db)):
    return ProductService(db).similar_products(product_id, min(max(limit, 1), 12))
@router.get("/{product_id}",response_model=ProductDetailRead)
def get_product(product_id:int,db:Session=Depends(get_db)):
    product=ProductService(db).get_product_detail(product_id)
    if not product: raise HTTPException(404,"Product not found")
    return product
