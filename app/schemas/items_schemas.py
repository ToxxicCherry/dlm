from pydantic import BaseModel
from typing import Optional
from .item_category_schemas import ItemCategory


class ItemBase(BaseModel):
    name: str
    quantity: float = 0
    description: Optional[str] = None


class ItemCreate(ItemBase):
    category_id: int


class ItemRead(ItemBase):
    id: int
    category: ItemCategory


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class ItemQuantity(BaseModel):
    item_id: int
    required_quantity: int


class QuantityChange(BaseModel):
    quantity: float
