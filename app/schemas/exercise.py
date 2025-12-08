from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class ExerciseBase(BaseModel):
    title: str
    desc: Optional[str] = None


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseUpdate(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None


class ExerciseOut(BaseModel):
    id: UUID
    title: str
    desc: Optional[str] = None

    class Config:
        from_attributes = True