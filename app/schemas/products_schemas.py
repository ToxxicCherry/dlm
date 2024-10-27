from pydantic import BaseModel
from typing import Optional, List
from app.schemas import ItemBase


class ProducItemBase(BaseModel):
    item_id: int
    required_quantity: int
    

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    items: Optional[List[ProducItemBase]] = None
    quantity: Optional[int] = None
    is_tempalted: Optional[bool] = True
    

    class Config:
        orm_mode = True
