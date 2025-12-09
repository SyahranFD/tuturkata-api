from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class BadgeOut(BaseModel):
    id: UUID
    user_id: UUID
    exercise_id: Optional[UUID] = None
    title: str
    icon_name: str
    desc: Optional[str] = None
    type: str
    updated_at: Optional[datetime] = None
    isCompleted: bool

    class Config:
        from_attributes = True