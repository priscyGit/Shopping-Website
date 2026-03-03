from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.item_schema import ItemCreate, ItemResponse
from app.services.items_service import create_item, get_all_items, get_item, delete_item

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=ItemResponse)
def create(data: ItemCreate, db: Session = Depends(get_db)):
    return create_item(data, db)

@router.get("/", response_model=list[ItemResponse])
def list_items(db: Session = Depends(get_db)):
    return get_all_items(db)

@router.get("/{item_id}", response_model=ItemResponse)
def get(item_id: int, db: Session = Depends(get_db)):
    item = get_item(item_id, db)

    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    return item


@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    item = delete_item(item_id, db)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}


