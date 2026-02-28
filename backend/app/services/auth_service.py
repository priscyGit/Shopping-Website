from fastapi import HTTPException
from passlib.hash import bcrypt
from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user_schema import UserLogin, UserCreate
from app.utils.session_manager import create_session


def register_user(data: UserCreate, db: Session):
    hashed_password = bcrypt.hash(data.password)
    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        email=data.email,
        phone=data.phone,
        country=data.country,
        city=data.city,
        username=data.username,
        password_hash =hashed_password
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def login_user(data: UserLogin, db: Session):
    user = db.query(User).filter(User.username == data.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not bcrypt.verify(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect password")

    token = create_session(user.id)

    return token

