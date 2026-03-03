from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order, OrderItem, OrderStatus
from app.models.item import Item


def get_temp_order(user_id: int, db: Session):
    return db.query(Order).filter(
        Order.user_id == user_id,
        Order.status == OrderStatus.TEMP
    ).first()


def create_temp_order(user_id: int, db: Session):
    order = Order(
        user_id=user_id,
        status=OrderStatus.TEMP,
        total_price=0
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def add_item_to_order(user_id: int, item_id: int, quantity: int, db: Session):
    order = get_temp_order(user_id, db)

    if not order:
        order = create_temp_order(user_id, db)

    if order.status != OrderStatus.TEMP:
        raise HTTPException(400, "Cannot modify closed order")

    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")

    if item.stock < quantity:
        raise HTTPException(400, "Not enough stock")

    order_item = OrderItem(
        order_id=order.id,
        item_id=item_id,
        quantity=quantity,
        price_at_purchase=item.price
    )
    db.add(order_item)

    order.total_price += item.price * quantity

    db.commit()
    db.refresh(order)
    return order


def remove_item_from_order(user_id: int, item_id: int, quantity: int, db: Session):
    order = get_temp_order(user_id, db)
    if not order:
        return None

    order_item = next((oi for oi in order.items if oi.item_id == item_id), None)
    if not order_item:
        return None

    # אם הכמות להסרה גדולה או שווה לכמות שיש – מוחקים את הפריט
    if quantity >= order_item.quantity:
        db.delete(order_item)
    else:
        order_item.quantity -= quantity

    db.commit()
    db.refresh(order)
    return order





def purchase_order(user_id: int, db: Session):
    order = get_temp_order(user_id, db)
    if not order:
        raise HTTPException(404, "No open order to purchase")

    if order.status != OrderStatus.TEMP:
        raise HTTPException(400, "Cannot modify a closed order")

    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    for oi in order_items:
        item = db.query(Item).filter(Item.id == oi.item_id).first()

        if item.stock < oi.quantity:
            raise HTTPException(400, f"Not enough stock for item {item.name}")

        item.stock -= oi.quantity

    order.status = OrderStatus.CLOSE

    db.commit()
    db.refresh(order)
    return order



def get_user_orders(user_id: int, db: Session):
    return db.query(Order).filter(Order.user_id == user_id).all()







