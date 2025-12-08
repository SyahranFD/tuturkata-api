from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel


class UserLevelBase(BaseModel):
    user_id: UUID
    level_id: UUID
    star: int
    accuration: int


class UserLevelCreate(UserLevelBase):
    pass


class UserLevelUpdate(BaseModel):
    user_id: Optional[UUID] = None
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