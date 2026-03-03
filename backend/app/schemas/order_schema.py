from pydantic import BaseModel,Field
from datetime import datetime



class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    name: str
    price: float
    quantity: int

class OrderResponse(BaseModel):
    id: int
    status: str
    total_price: float
    shipping_address: str | None
    order_date: datetime
    items: list[OrderItemResponse]

class OrderItemUpdate(BaseModel):
    item_id: int
    quantity: int


