import uuid
from sqlalchemy import Column, String, Text, Integer
from sqlalchemy.dialects.postgresql import UUID

from ..config.database import Base


class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order = Column(Integer, nullable=False)
    title = Column(String(100), nullable=False)
    desc = Column(Text, nullable=True)