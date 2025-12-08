import uuid
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from ..config.database import Base


class UserExercise(Base):
    __tablename__ = 'user_exercise'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    exercise_id = Column(UUID(as_uuid=True), ForeignKey('exercise.id', ondelete='CASCADE'), nullable=False)
    max_level = Column(Integer, nullable=False)
    current_level = Column(Integer, nullable=False)