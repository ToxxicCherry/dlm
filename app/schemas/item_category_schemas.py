from pydantic import BaseModel


class ItemCategoryBase(BaseModel):
    name: str


class ItemCategory(ItemCategoryBase):
    id: int

    class Config:
        orm_mode = True


class ItemCategoryCreate(ItemCategoryBase):
    pass
