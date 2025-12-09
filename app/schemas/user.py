from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field, field_serializer


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr
    exp: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

    @field_serializer('created_at', when_used='json')
    def serialize_created_at(self, value: datetime) -> str:
        return value.strftime('%Y-%m-%d')

    @field_serializer('updated_at', when_used='json')
    def serialize_updated_at(self, value: datetime) -> str:
        return value.strftime('%Y-%m-%d')


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"