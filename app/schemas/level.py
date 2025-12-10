from typing import Optional
from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field, field_serializer


class LevelBase(BaseModel):
    exercise_id: UUID
    order: int
    title: str
    desc: Optional[str] = None


class LevelCreate(LevelBase):
    pass


class LevelUpdate(BaseModel):
    exercise_id: Optional[UUID] = None
    order: Optional[int] = None
    title: Optional[str] = None
    desc: Optional[str] = None


class LevelOut(BaseModel):
    id: UUID
    exercise_id: UUID
    order: int
    title: str
    desc: Optional[str] = None

    class Config:
        from_attributes = True


class LevelWithCompletionOut(BaseModel):
    level_id: UUID
    order: int
    title: str
    desc: Optional[str] = None
    star: int
    accuration: int
    updated_at: Optional[datetime] = None
    is_completed: bool = Field(..., alias="isCompleted")

    class Config:
        from_attributes = True

    @field_serializer('updated_at', when_used='json')
    def serialize_updated_at(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime('%Y-%m-%d') if value else None