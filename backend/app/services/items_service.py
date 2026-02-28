from sqlalchemy.orm import Session
from app.models.item import Item
from app.schemas.item_schema import ItemCreate

def create_item(data: ItemCreate, db: Session):
    item = Item(**data.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

def get_all_items(db: Session):
    return db.query(Item).all()

def get_item(item_id: int, db: Session):
    return db.query(Item).filter(Item.id == item_id).first()

def delete_item(item_id: int, db: Session):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        db.delete(item)
        db.commit()
    return item
