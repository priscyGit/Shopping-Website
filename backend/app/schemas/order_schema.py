from pydantic import BaseModel
from datetime import datetime
from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    item_id: int
    quantity: int


class OrderItemResponse(BaseModel):
    id: int
    item_id: int
    quantity: int
    price_at_purchase: float

    model_config = {"from_attributes": True}


class OrderResponse(BaseModel):
    id: int
    user_id: int
    date: datetime
    shipping_address: str | None
    total_price: float
    status: OrderStatus
    items: list[OrderItemResponse]

    model_config = {"from_attributes": True}
