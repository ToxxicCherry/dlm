from fastapi import HTTPException
from passlib.context import CryptContext
from . import models, schemas
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


async def get_user_by_email(db: AsyncSession, email: str) -> models.User:
    result = await db.execute(select(models.User).filter(models.User.email == email))
    return result.scalars().first()


async def get_user_by_username(db: AsyncSession, username: str) -> models.User:
    result = await db.execute(select(models.User).filter(models.User.username == username))
    return result.scalars().first()


async def get_user_by_id(db: AsyncSession, user_id: int) -> models.User:
    result = await db.execute(select(models.User).filter(models.User.id == user_id))
    return result.scalars().first()


async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    hashed_password = pwd_context.hash(user.password)

    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password,
        first_name=user.first_name,
        last_name=user.last_name
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def get_items(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(models.Item)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def get_item_by_id(db: AsyncSession, item_id: int):
    result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
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
    db_item = models.Item(**item.dict())

    result = await db.execute(select(models.Item).filter(models.Item.name == db_item.name))
    existing_item = result.scalars().first()

    if existing_item:
        raise HTTPException(status_code=400, detail="Item already exists")

    db.add(db_item)
    await db.commit()
    await db.refresh(db_item)
    return db_item


async def add_item_quantity(db: AsyncSession, item_id: int, quantity: int) -> models.Item:
    result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
    db_item = result.scalars().first()

    if db_item:
        db_item.quantity += quantity
        await db.commit()
        await db.refresh(db_item)
    return db_item


async def subtract_item_quantity(db: AsyncSession, item_id: int, quantity: int) -> models.Item:
    result = await db.execute(select(models.Item).filter(models.Item.id == item_id))
    db_item = result.scalars().first()

    if db_item:
        db_item.quantity -= quantity
        await db.commit()
        await db.refresh(db_item)
    return db_item


async def get_item_by_name(db: AsyncSession, item_name: str) -> models.Item:
    result = await db.execute(select(models.Item).filter(models.Item.name == item_name))
    return result.scalars().first()
