import uuid
from sqlalchemy import Column, String, Integer, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID

from ..config.database import Base
from ..utils.time import wib_now


class DailyMission(Base):
    __tablename__ = "daily_mission"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(100), nullable=False)
    type = Column(String(50), nullable=False)
    max_progress = Column(Integer, nullable=False)
    current_progress = Column(Integer, nullable=False, default=0)
    is_completed = Column('isCompleted', Boolean, nullable=False, default=False)
    # Store updated_at in WIB (UTC+7)
    updated_at = Column(DateTime, nullable=False, default=wib_now, onupdate=wib_now)

    @property
    def isCompleted(self):
        return self.is_completed

    @property
    def updated_at_formatted(self):
        return self.updated_at.strftime("%Y-%m-%d") if self.updated_at else None