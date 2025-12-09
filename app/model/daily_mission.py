import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from ..config.database import Base


class DailyMission(Base):
    __tablename__ = "daily_mission"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    max_progress = Column(Integer, nullable=False)
    current_progress = Column(Integer, nullable=False, default=0)
    is_completed = Column('isCompleted', Boolean, nullable=False, default=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)

    @property
    def isCompleted(self):
        return self.is_completed