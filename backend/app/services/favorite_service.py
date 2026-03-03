from sqlalchemy.orm import Session
from app.models.favorite import Favorite
from fastapi import HTTPException


def add_favorite(user_id: int, item_id: int, db: Session):
    existing = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.item_id == item_id
    ).first()

    if existing:
        return existing

    favorite = Favorite(
        user_id=user_id,
        item_id=item_id
    )

    db.add(favorite)
    db.commit()
    db.refresh(favorite)
    return favorite

def get_user_favorites(user_id: int, db: Session):
    return db.query(Favorite).filter(Favorite.user_id == user_id).all()


def delete_favorite(db: Session, favorite_id: int, user_id: int):
    favorite = db.query(Favorite).filter(
        Favorite.id == favorite_id,
        Favorite.user_id == user_id
    ).first()

    if not favorite:
        raise HTTPException(status_code=404, detail="Favorite not found")

    db.delete(favorite)
    db.commit()
    return {"message": "Favorite deleted successfully"}



