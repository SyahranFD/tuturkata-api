import uuid
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID

from ..config.database import Base


class Level(Base):
    __tablename__ = "level"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exercise_id = Column(UUID(as_uuid=True), ForeignKey("exercise.id", ondelete="CASCADE"), nullable=False)
    order = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    desc = Column(Text, nullable=True)