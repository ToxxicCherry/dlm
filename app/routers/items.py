from typing import List, Type
from fastapi import APIRouter, Depends, HTTPException
from app.database import get_db
from app import schemas, models, dependencies, crud, auth
from app.models import Item
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


@router.post('/{item_id}/add/', response_model=schemas.Item)
async def add_item_quantity(
        item_id: int,
        quantity_change: schemas.QuantityChange,
        db: AsyncSession = Depends(get_db),
        current_user: models.User = Depends(dependencies.admin_required)
):
    try:
        db_item = await crud.add_item_quantity(db=db, item_id=item_id, quantity=quantity_change.quantity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.post('/{item_id}/subtract/', response_model=schemas.Item)
async def subtract_item_quantity(
        item_id: int,
        quantity_change: schemas.QuantityChange,
        db: AsyncSession = Depends(get_db),
        current_user: models.User = Depends(dependencies.admin_required)
):
    try:
        db_item = await crud.subtract_item_quantity(db=db, item_id=item_id, quantity=quantity_change.quantity)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get('/{item_id}/', response_model=schemas.Item)
async def read_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_item = await crud.get_item_by_id(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.put('/{item_id}/', response_model=schemas.Item)
async def update_item(
        item_id: int,
        item: schemas.ItemCreate,
        db: AsyncSession = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_item = await crud.update_item(db=db, item_id=item_id, item=item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.delete('/{item_id}/', response_model=schemas.Item)
async def delete_item(
        item_id: int,
        db: AsyncSession = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    db_item = await crud.delete_item(db=db, item_id=item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.get('/', response_model=List[schemas.Item])
async def read_items(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db),
        #current_user: models.User = Depends(auth.get_current_user),
) -> list[Type[Item]]:

    return await crud.get_items(db, skip=skip, limit=limit)


@router.post('/', response_model=schemas.Item)
async def create_item(
        item: schemas.ItemCreate,
        db: AsyncSession = Depends(get_db),
        current_user: models.User = Depends(auth.get_current_user)
):
    return await crud.create_item(db=db, item=item)
