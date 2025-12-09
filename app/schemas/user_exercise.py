from uuid import UUID
from pydantic import BaseModel


class UserExerciseOut(BaseModel):
    id: UUID
    user_id: UUID
    exercise_id: UUID
    max_level: int
    current_level: int

    class Config:
        from_attributes = True


class UserExerciseWithExerciseOut(BaseModel):
    exercise_id: UUID
    max_level: int
    current_level: int
    title: str | None = None
    desc: str | None = None

    class Config:
        from_attributes = True