from uuid import UUID
from pydantic import BaseModel


class LevelQuizBase(BaseModel):
    level_id: UUID
    order: int
    instruction: str
    speech_text: str
    exp: int


class LevelQuizCreate(LevelQuizBase):
    pass


class LevelQuizUpdate(BaseModel):
    level_id: UUID | None = None
    order: int | None = None
    instruction: str | None = None
    speech_text: str | None = None
    exp: int | None = None


class LevelQuizOut(BaseModel):
    id: UUID
    level_id: UUID
    order: int
    instruction: str
    speech_text: str
    exp: int

    class Config:
        from_attributes = True