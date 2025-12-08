from uuid import UUID
from pydantic import BaseModel


class LevelQuizBase(BaseModel):
    level_id: UUID
    order: int
    instruction: str
    question: str


class LevelQuizCreate(LevelQuizBase):
    pass


class LevelQuizUpdate(BaseModel):
    level_id: UUID | None = None
    order: int | None = None
    instruction: str | None = None
    question: str | None = None


class LevelQuizOut(BaseModel):
    id: UUID
    level_id: UUID
    order: int
    instruction: str
    question: str

    class Config:
        from_attributes = True