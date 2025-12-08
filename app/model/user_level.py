import uuid
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..config.database import Base


class UserLevel(Base):
    __tablename__ = 'user_level'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    level_id = Column(UUID(as_uuid=True), ForeignKey('level.id', ondelete='CASCADE'), nullable=False)
    star = Column(Integer, nullable=False)
    accuration = Column(Integer, nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), nullable=False)
