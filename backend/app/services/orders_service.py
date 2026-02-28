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
    # 1) למצוא TEMP order
    order = get_temp_order(user_id, db)

    # 2) אם אין — ליצור
    if not order:
        order = create_temp_order(user_id, db)

    # 3) בדיקת מלאי
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(404, "Item not found")

    if item.stock < quantity:
        raise HTTPException(400, "Not enough stock")

    # 4) הוספת פריט להזמנה
    order_item = OrderItem(
        order_id=order.id,
        item_id=item_id,
        quantity=quantity,
        price_at_purchase=item.price
    )
    db.add(order_item)

    # 5) עדכון מחיר כולל
    order.total_price += item.price * quantity

    db.commit()
    db.refresh(order)
    return order


def remove_item_from_order(user_id: int, item_id: int, db: Session):
    order = db.query(Order).filter(
        Order.user_id == user_id,
        Order.status == OrderStatus.TEMP
    ).first()

    if not order:
        return None

    order_item = db.query(OrderItem).filter(
        OrderItem.order_id == order.id,
        OrderItem.item_id == item_id
    ).first()

    if not order_item:
        return order

    db.delete(order_item)
    db.commit()

    order.total_price = sum(oi.price_at_purchase * oi.quantity for oi in order.items)
    db.commit()
    db.refresh(order)

    return order



def purchase_order(user_id: int, db: Session):
    # 1) למצוא TEMP order
    order = get_temp_order(user_id, db)
    if not order:
        raise HTTPException(404, "No open order to purchase")

    # 2) לעדכן מלאי
    order_items = db.query(OrderItem).filter(OrderItem.order_id == order.id).all()

    for oi in order_items:
        item = db.query(Item).filter(Item.id == oi.item_id).first()

        if item.stock < oi.quantity:
            raise HTTPException(400, f"Not enough stock for item {item.name}")

        item.stock -= oi.quantity

    # 3) לשנות סטטוס ל־CLOSE
    order.status = OrderStatus.CLOSE

    db.commit()
    db.refresh(order)
    return order


def get_user_orders(user_id: int, db: Session):
    return db.query(Order).filter(Order.user_id == user_id).all()
