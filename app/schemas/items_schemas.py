from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    quantity: float = 0


class Item(ItemBase):
    id: int
    quantity: float

    class Config:
        orm_mode = True


class ItemQuantity(BaseModel):
    item_id: int
    required_quantity: int


class QuantityChange(BaseModel):
    quantity: int
