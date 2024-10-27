from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException, status
from app import schemas
from app import models


async def get_existing_product_template(db: AsyncSession, name: str) -> models.Product:
    result = await db.execute(select(models.Product).where(models.Product.name == name, models.Product.is_template == True))
    return result.scalars().first()



async def create_product_template_crud(db: AsyncSession, product_data: schemas.ProductTemplateCreate) -> schemas.ProductTemplateCreate:
    
    new_product = models.Product(
        name=product_data.name,
        description=product_data.description
    )
    db.add(new_product)
    await db.flush()
    
    for item in product_data.items:
        item_obj = await db.execute(select(models.Item).where(models.Item.id == item.item_id))
        item_obj = item_obj.scalars().first()

        if not item_obj:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Item {item.item_id} not found")
        
        product_item = models.ProductItem(
            product_id=new_product.id,
            item_id=item_obj.id,
            required_quantity=item.required_quantity
        )
        
        db.add(product_item)
    
    await db.commit()
    await db.refresh(new_product)
    return product_data
