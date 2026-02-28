from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str | None = None
    country: str | None = None
    city: str | None = None
    username: str

class UserCreate(UserBase):
    password: str = Field(..., max_length=72)

class UserLogin(BaseModel):
    username: str
    password: str

class UserResponse(UserBase):
    id: int

    model_config = {"from_attributes": True}

