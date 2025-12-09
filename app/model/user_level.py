import uuid
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..config.database import Base
from ..utils.time import wib_now


class UserLevel(Base):
    __tablename__ = 'user_level'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    level_id = Column(UUID(as_uuid=True), ForeignKey('level.id', ondelete='CASCADE'), nullable=False)
    star = Column(Integer, nullable=False)
    accuration = Column(Integer, nullable=False)
    # Store timestamps in WIB (UTC+7)
    created_at = Column(DateTime, nullable=False, default=wib_now)
    updated_at = Column(DateTime, nullable=False, default=wib_now, onupdate=wib_now)

    # Formatted date properties for response serialization
    @property
    def created_at_formatted(self):
        return self.created_at.strftime("%Y-%m-%d") if self.created_at else None

    @property
    def updated_at_formatted(self):
        return self.updated_at.strftime("%Y-%m-%d") if self.updated_at else None
