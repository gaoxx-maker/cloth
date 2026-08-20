from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.product import ProductRead
from app.services.product_service import ProductService
router=APIRouter(prefix="/products",tags=["products"])
@router.get("",response_model=list[ProductRead])
def list_products(limit:int=20,offset:int=0,db:Session=Depends(get_db)): return ProductService(db).list_products(limit,offset)
@router.get("/{product_id}",response_model=ProductRead)
def get_product(product_id:int,db:Session=Depends(get_db)):
    product=ProductService(db).get_product(product_id)
    if not product: raise HTTPException(404,"Product not found")
    return product
