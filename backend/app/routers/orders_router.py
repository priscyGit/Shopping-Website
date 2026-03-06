from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.order_schema import OrderItemCreate, OrderResponse ,OrderItemUpdate
from app.services.orders_service import (
    add_item_to_order,
    remove_item_from_order,
    purchase_order,
    get_user_orders,
    get_temp_order
)
from app.utils.jwt_handler import get_current_user
from app.models.user import User


router = APIRouter(prefix="/orders", tags=["Orders"])


def serialize_order(order):
    return {
        "id": order.id,
        "status": order.status,
        "total_price": order.total_price,
        "shipping_address": order.shipping_address,
        "order_date": order.date,
        "items": [
            {
                "item_id": oi.item_id,
                "name": oi.item.name,
                "price": oi.price_at_purchase,
                "quantity": oi.quantity,

            }
            for oi in order.items

    ]
    }


@router.post("/add-item", response_model=OrderResponse)
def add_item(data:  OrderItemCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    order = add_item_to_order(user.id, data.item_id, data.quantity, db)
    return serialize_order(order)




@router.post("/remove-item", response_model=OrderResponse)
def remove_item(
    data: OrderItemUpdate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = remove_item_from_order(user.id, data.item_id, data.quantity, db)
    if not order:
        raise HTTPException(404, "No open order found")
    return serialize_order(order)




@router.post("/purchase", response_model=OrderResponse)
def purchase(user=Depends(get_current_user), db: Session = Depends(get_db)):
    order = purchase_order(user.id, db)
    if not order:
        raise HTTPException(404, "No open order to purchase")
    return serialize_order(order)



@router.get("/", response_model=list[OrderResponse])
def list_orders(user=Depends(get_current_user), db: Session = Depends(get_db)):
    orders = get_user_orders(user.id, db)
    return [serialize_order(order) for order in orders]



@router.get("/current", response_model=OrderResponse)
def get_current_order(user=Depends(get_current_user), db: Session = Depends(get_db)):
    order = get_temp_order(user.id, db)
    if not order:
        raise HTTPException(404, "No open order found")
    return serialize_order(order)


@router.get("/users")
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [
        {
            "id": u.id,
            "username": u.username,
            "email": u.email,

        }
        for u in users
    ]

