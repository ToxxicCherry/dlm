from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app import schemas
from app import models


async def create_product(db: AsyncSession, product: schemas.ProductCreate) -> models.Product:
    db_product = models.Product(**product.dict())

    result = await db.execute(select(models.Product).filter(models.Product.name == db_product.name))


async def get_product_template_by_name(db: AsyncSession, name: str) -> models.ProductTemplate:
    result = await db.execute(select(models.ProductTemplate).filter(models.ProductTemplate.name == name))
    return result.scalar().first()


async def create_product_template(db: AsyncSession)
