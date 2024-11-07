from sqlalchemy.ext.asyncio import AsyncSession
from ..models import ItemCategory
from sqlalchemy import select


async def get_item_categories(db: AsyncSession, skip: int = 0, limit: int = 10):
    result = await db.execute(
        select(ItemCategory)
        .offset(skip)
        .limit(limit))
    return result.scalars().all()


async def get_category_by_id(db: AsyncSession, cat_id: int):
    category = await db.execute(select(ItemCategory).where(ItemCategory.id == cat_id))
    return category.scalars().first()
