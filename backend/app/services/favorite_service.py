from sqlalchemy.orm import Session
from app.models.favorite import Favorite

def add_favorite(user_id: int, item_id: int, db: Session):
    existing = db.query(Favorite).filter(
        Favorite.user_id == user_id,
        Favorite.item_id == item_id
    ).first()

    if existing:
        return existing  # לא מוסיפים פעמיים

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


def delete_favorite(favorite_id: int, user_id: int, db: Session):
    favorite = db.query(Favorite).filter(
        Favorite.id == favorite_id,
        Favorite.user_id == user_id
    ).first()

    if not favorite:
        return None

    db.delete(favorite)
    db.commit()
    return favorite


