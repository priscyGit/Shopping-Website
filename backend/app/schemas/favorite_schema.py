from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    item_id: int

class FavoriteResponse(BaseModel):
    id: int
    item_id: int
    name: str
    price: float

    class Config:
        orm_mode = True
