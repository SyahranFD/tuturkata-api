import uuid
from sqlalchemy import Column, Text, ForeignKey, Integer
from sqlalchemy.dialects.postgresql import UUID

from ..config.database import Base


class LevelQuiz(Base):
    __tablename__ = "level_quiz"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    level_id = Column(UUID(as_uuid=True), ForeignKey("level.id", ondelete="CASCADE"), nullable=False)
    order = Column(Integer, nullable=False)
    instruction = Column(Text, nullable=False)
    speech_text = Column(Text, nullable=False)
    exp = Column(Integer, nullable=False, server_default='0')