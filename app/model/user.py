import uuid
from sqlalchemy import Column, String, DateTime, Integer
from sqlalchemy.dialects.postgresql import UUID

from ..config.database import Base
from ..utils.time import wib_now


class User(Base):
    __tablename__ = "user"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), nullable=False)
    email = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    exp = Column(Integer, nullable=False, server_default='0')
    streak = Column(Integer, nullable=False, server_default='0')
    # Store timestamps in WIB (UTC+7), using application-side defaults
    created_at = Column(DateTime, nullable=False, default=wib_now)
    updated_at = Column(DateTime, nullable=False, default=wib_now, onupdate=wib_now)

    # Formatted date properties for response serialization
    @property
    def created_at_formatted(self):
        return self.created_at.strftime("%Y-%m-%d") if self.created_at else None

    @property
    def updated_at_formatted(self):
        return self.updated_at.strftime("%Y-%m-%d") if self.updated_at else None