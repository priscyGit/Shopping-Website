from pydantic import BaseModel

class FavoriteCreate(BaseModel):
    item_id: int

class FavoriteResponse(BaseModel):
    id: int
    item_id: int
