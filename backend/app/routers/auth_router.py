from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.auth_service import register_user, login_user
from fastapi.responses import JSONResponse


router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return register_user(user, db)

@router.post("/login")
def login(data: UserLogin, db: Session = Depends(get_db)):
    token = login_user(data, db)

    response = JSONResponse({"message": "Login successful"})
    response.set_cookie(
        key="session_token",
        value=token,
        httponly=True,
        samesite="lax"
    )
    return response


