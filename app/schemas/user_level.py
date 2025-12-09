from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, field_serializer


class UserLevelBase(BaseModel):
    level_id: UUID
    star: int
    accuration: int
    exp: int


class UserLevelCreate(UserLevelBase):
    pass


class UserLevelUpdate(BaseModel):
    level_id: Optional[UUID] = None
    star: Optional[int] = None
    accuration: Optional[int] = None


class UserLevelOut(BaseModel):
    id: UUID
    user_id: UUID
    level_id: UUID
    star: int
    accuration: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

    @field_serializer('created_at', when_used='json')
    def serialize_created_at(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime('%Y-%m-%d') if value else None

    @field_serializer('updated_at', when_used='json')
    def serialize_updated_at(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime('%Y-%m-%d') if value else None