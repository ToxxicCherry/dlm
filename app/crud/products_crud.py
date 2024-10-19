from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import schemas
from app import models


async def create_product(db: AsyncSession, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(**product.dict())

    result = await db.execute(select(models.Product).filter(models.Product.name == db_product.name))
    existing