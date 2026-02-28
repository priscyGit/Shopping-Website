from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.favorite_schema import FavoriteCreate, FavoriteResponse
from app.services.favorite_service import add_favorite, get_user_favorites, delete_favorite

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.post("/", response_model=FavoriteResponse)
def create_favorite(
    data: FavoriteCreate,
    request: Request,
    db: Session = Depends(get_db)
):
    if request.state.user_id is None:
        raise HTTPException(status_code=401, detail="Login required")

    return add_favorite(request.state.user_id, data.item_id, db)

@router.get("/", response_model=list[FavoriteResponse])
def list_favorites(
    request: Request,
    db: Session = Depends(get_db)
):
    if request.state.user_id is None:
        raise HTTPException(status_code=401, detail="Login required")

    return get_user_favorites(request.state.user_id, db)

@router.delete("/{favorite_id}")
def remove_favorite(favorite_id: int, request: Request, db: Session = Depends(get_db)):
    if request.state.user_id is None:
        raise HTTPException(401, "Login required")

    favorite = delete_favorite(favorite_id, request.state.user_id, db)
    if not favorite:
        raise HTTPException(404, "Favorite not found")

    return {"detail": "Favorite removed"}


