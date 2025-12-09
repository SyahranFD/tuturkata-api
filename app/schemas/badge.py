from typing import Optional
from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, Field, field_serializer


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

    @field_serializer('updated_at', when_used='json')
    def serialize_updated_at(self, value: Optional[datetime]) -> Optional[str]:
        return value.strftime('%Y-%m-%d') if value else None