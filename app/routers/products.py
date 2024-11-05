from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.products_schemas import *
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.crud.products_crud import *
from app.dependencies import admin_required


router = APIRouter()

@router.post('/product_template/', response_model=ProductTemplateCreate, status_code=status.HTTP_201_CREATED)
async def create_product_template(
    product_data: ProductTemplateCreate, 
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(admin_required)
):
    
    exist_product_template = await get_existing_product_template_by_name(db, name=product_data.name)

    if exist_product_template:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Product template {product_data.name} already exists")
    
    
    return await create_product_template_crud(db, product_data)


@router.delete('/{product_template_id}/')
async def delete_product_template(
    product_template_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: models.User = Depends(admin_required)
):
    exsit_product_template = await get_existing_product_template_by_id(db, id=product_template_id)
    
    if not exsit_product_template:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Product template {product_template_id} not found")
    
    return await delete_product_template_crud(db, product_template_id)