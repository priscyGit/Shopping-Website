from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item_schema import ItemCreate
import json
from app.db.redis_client import redis_client


def create_item(data: ItemCreate, db: Session):
    item = Item(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_all_items(db: Session):
    cached = redis_client.get("items")
    if cached:
        return json.loads(cached)

    items = db.query(Item).all()

    items_data = [
        {
            "id": item.id,
            "name": item.name,
            "price": item.price,
            "stock": item.stock
        }
        for item in items
    ]

    redis_client.set("items", json.dumps(items_data), ex=60)
    return items_data



def get_item(item_id: int, db: Session):
    return db.query(Item).filter(Item.id == item_id).first()

def delete_item(item_id: int, db: Session):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item
