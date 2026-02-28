from pydantic import BaseModel

class FavoriteBase(BaseModel):
    user_id: int
    item_id: int

class FavoriteCreate(FavoriteBase):
    pass

class FavoriteResponse(FavoriteBase):
    id: int

    model_config = {"from_attributes": True}
