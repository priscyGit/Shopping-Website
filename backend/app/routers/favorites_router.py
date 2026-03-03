from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.favorite_schema import FavoriteCreate, FavoriteResponse
from app.services.favorite_service import add_favorite, get_user_favorites, delete_favorite
from app.utils.jwt_handler import get_current_user

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/", response_model=FavoriteResponse)
def create_favorite(
    data: FavoriteCreate,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    favorite = add_favorite(user.id, data.item_id, db)
    return {
        "id": favorite.id,
        "item_id": favorite.item_id
    }

@router.get("/", response_model=list[FavoriteResponse])
def list_favorites(
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    favorites = get_user_favorites(user.id, db)
    return [
        {
            "id": fav.id,
            "item_id": fav.item_id,
            "name": fav.item.name,
            "price": fav.item.price
        }
        for fav in favorites
    ]

@router.delete("/{favorite_id}", status_code=204)
def remove_favorite(
    favorite_id: int,
    user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    delete_favorite(db, favorite_id, user.id)
    return
