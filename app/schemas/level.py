from typing import Optional
from uuid import UUID
from pydantic import BaseModel


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