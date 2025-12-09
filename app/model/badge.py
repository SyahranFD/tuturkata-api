import uuid
from sqlalchemy import Column, String, Text, Boolean, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ..config.database import Base


class Badge(Base):
    __tablename__ = "badge"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercise.id", ondelete="SET NULL"), nullable=True)
    title = Column(String(100), nullable=False)
    icon_name = Column(String(100), nullable=False)
    desc = Column(Text, nullable=True)
    type = Column(String(50), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)
    is_completed = Column('isCompleted', Boolean, nullable=False, default=False)

    @property
    def isCompleted(self):
        return self.is_completed