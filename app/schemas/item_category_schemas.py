from pydantic import BaseModel


class ItemCategoryBase(BaseModel):
    name: str


class ItemCategory(ItemCategoryBase):
    id: int


class ItemCategoryCreate(ItemCategoryBase):
    pass
