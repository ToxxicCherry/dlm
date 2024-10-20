from pydantic import BaseModel
from typing import Optional


class ItemBase(BaseModel):
    name: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class ItemInProductTemplate(BaseModel):
    item_id: int
    quantity_needed: int


class QuantityChange(BaseModel):
    quantity: int
