from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.order_schema import OrderItemCreate, OrderResponse
from app.services.orders_service import (
    add_item_to_order,
    remove_item_from_order,
    purchase_order,
    get_user_orders,
    get_temp_order
)

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/add-item", response_model=OrderResponse)
def add_item(data: OrderItemCreate, request: Request, db: Session = Depends(get_db)):
    if request.state.user_id is None:
        raise HTTPException(401, "Login required")

    return add_item_to_order(request.state.user_id, data.item_id, data.quantity, db)


@router.delete("/remove-item/{item_id}", response_model=OrderResponse)
def remove_item(item_id: int, request: Request, db: Session = Depends(get_db)):
    if request.state.user_id is None:
        raise HTTPException(401, "Login required")

    order = remove_item_from_order(request.state.user_id, item_id, db)
    if not order:
        raise HTTPException(404, "No open order found")

    return remove_item_from_order(request.state.user_id, item_id, db)


@router.post("/purchase", response_model=OrderResponse)
def purchase(request: Request, db: Session = Depends(get_db)):
    if request.state.user_id is None:
        raise HTTPException(401, "Login required")

    order = purchase_order(request.state.user_id, db)
    if not order:
        raise HTTPException(404, "No open order to purchase")

    return order



@router.get("/", response_model=list[OrderResponse])
def list_orders(request: Request, db: Session = Depends(get_db)):
    if request.state.user_id is None:
        raise HTTPException(401, "Login required")

    return get_user_orders(request.state.user_id, db)


@router.get("/current", response_model=OrderResponse)
def get_current_order(request: Request, db: Session = Depends(get_db)):
    if request.state.user_id is None:
        raise HTTPException(401, "Login required")

    order = get_temp_order(request.state.user_id, db)
    if not order:
        raise HTTPException(404, "No open order found")

    return order

