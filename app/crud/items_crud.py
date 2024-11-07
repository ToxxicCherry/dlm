from sqlalchemy.ext.asyncio import AsyncSession
from .. import models, schemas
from sqlalchemy import select
from sqlalchemy.orm import joinedload
from fastapi import HTTPException, status
from .item_category_crud import get_category_by_id


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Item)
        .options(joinedload(models.Item.category))
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_item_by_id(db: AsyncSession, item_id: int):
    result = await db.execute(
        select(models.Item)
        .options(joinedload(models.Item.category))
        .filter(models.Item.id == item_id))
    return result.scalars().first()


async def update_item(db: AsyncSession, item_id: int, item: schemas.ItemCreate) -> models.Item:
    db_item = await get_item_by_id(db, item_id)
    if db_item:
        for key, value in item.dict().items():
            setattr(db_item, key, value)
        await db.commit()
        await db.refresh(db_item)

    return db_item


async def delete_item(db: AsyncSession, item_id: int) -> models.Item:
    db_item = await get_item_by_id(db, item_id)
    if db_item:
        await db.delete(db_item)
        await db.commit()
    return db_item


async def create_item(db: AsyncSession, item: schemas.ItemCreate) -> models.Item:
    category_instance = await get_category_by_id(db, item.category_id)

    if not category_instance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Category not found')

    existing_item = await get_item_by_name(db, item.name)

    if existing_item:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists")

    db_item = models.Item(
        name=item.name,
        quantity=item.quantity,
        description=item.description,
        category=category_instance
    )

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def add_item_quantity(db: AsyncSession, item_id: int, quantity: int) -> models.Item:
    result = await db.execute(
        select(models.Item)
        .options(joinedload(models.Item.category))
        .filter(models.Item.id == item_id))
    db_item = result.scalars().first()

    if db_item:
        db_item.quantity += quantity
        await db.commit()
        await db.refresh(db_item)
    return db_item


async def subtract_item_quantity(db: AsyncSession, item_id: int, quantity: int) -> models.Item:
    result = await db.execute(
        select(models.Item)
        .options(joinedload(models.Item.category))
        .filter(models.Item.id == item_id))
    db_item = result.scalars().first()

    if db_item:
        db_item.quantity -= quantity
        await db.commit()
        await db.refresh(db_item)
    return db_item


async def get_item_by_name(db: AsyncSession, item_name: str) -> models.Item:
    result = await db.execute(select(models.Item).filter(models.Item.name == item_name))
    return result.scalars().first()
