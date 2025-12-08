from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ExerciseBase(BaseModel):
    order: int
    title: str
    desc: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    order: Optional[int] = None
    title: Optional[str] = None
    desc: Optional[str] = None


class ExerciseOut(BaseModel):
    id: UUID
    order: int
    title: str
    desc: Optional[str] = None

    class Config:
        from_attributes = True