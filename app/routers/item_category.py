from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from ..database import get_db
from ..schemas.item_category_schemas import ItemCategory as ICSchema
from ..crud.item_category_crud import *
from typing import List, Optional, Type


router = APIRouter()


@router.get('/', response_model=List[ICSchema])
async def read_item_categories(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    return await get_item_categories(db, skip=skip, limit=limit)