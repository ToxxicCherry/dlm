from pydantic import BaseModel
from typing import Optional, List
from app.schemas import ItemBase, ItemInProductTemplate


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    quantity: Optional[int] = None
    items: Optional[List[ItemBase]] = None

    class Config:
        orm_mode = True


class ProductTemplateBase(BaseModel):
    name: str
    description: Optional[str] = None
    items: Optional[List[ItemInProductTemplate]] = []


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    id: int
