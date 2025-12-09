from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel


class DailyMissionOut(BaseModel):
    id: UUID
    title: str
    type: str
    max_progress: int
    current_progress: int
    isCompleted: bool
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True