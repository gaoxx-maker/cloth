from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.dependencies import get_db
from app.schemas.product import ProductRead
from app.services.search_service import SearchService
router=APIRouter(prefix="/search",tags=["search"])
@router.get("",response_model=list[ProductRead])
def search(q:str,limit:int=20,db:Session=Depends(get_db)): return SearchService(db).search(q,limit)
