from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.products_schemas import ProductTemplateCreate
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud.products_crud import *


router = APIRouter()

@router.post('/product_template/', response_model=ProductTemplateCreate, status_code=status.HTTP_201_CREATED)
async def create_product_template(product_data: ProductTemplateCreate, db: AsyncSession = Depends(get_db)):
    exist_product_template = await get_existing_product_template(db, name=product_data.name)

    if exist_product_template:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product template {product_data.name} already exists")
    
    
    return await create_product_template_crud(db, product_data)