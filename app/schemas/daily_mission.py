from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer


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

    # Serialize datetime to YYYY-MM-DD on JSON output
    @field_serializer('updated_at', when_used='json')
    def serialize_updated_at(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime('%Y-%m-%d') if value else None