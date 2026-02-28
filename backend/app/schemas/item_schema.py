from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    price: float
    stock: int

class ItemCreate(ItemBase):
    pass

class ItemResponse(ItemBase):
    id: int

    model_config = {"from_attributes": True}
