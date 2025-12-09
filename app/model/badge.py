import uuid
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..config.database import Base
from ..utils.time import wib_now


class Badge(Base):
    __tablename__ = "badge"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercise.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(100), nullable=False)
    icon_name = Column(String(100), nullable=False)
    desc = Column(Text, nullable=True)
    type = Column(String(50), nullable=False)
    # Store updated_at in WIB (UTC+7)
    updated_at = Column(DateTime, nullable=False, default=wib_now, onupdate=wib_now)
    is_completed = Column('isCompleted', Boolean, nullable=False, default=False)

    @property
    def isCompleted(self):
        return self.is_completed

    @property
    def updated_at_formatted(self):
        return self.updated_at.strftime("%Y-%m-%d") if self.updated_at else None