import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..model.level import Level
from ..model.exercise import Exercise
from ..schemas.level import LevelCreate, LevelUpdate


def get_level_by_id(db: Session, level_id: str) -> Optional[Level]:
    return db.query(Level).filter(Level.id == level_id).first()


def get_all_levels(db: Session) -> List[Level]:
    return db.query(Level).order_by(Level.order.asc()).all()


def get_levels_by_exercise_id(db: Session, exercise_id: str) -> List[Level]:
    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return (
        db.query(Level)
        .filter(Level.exercise_id == exercise_id)
        .order_by(Level.order.asc())
        .all()
    )


def create_level(db: Session, payload: LevelCreate) -> Level:
    # Validasi parent exercise
    exercise = db.query(Exercise).filter(Exercise.id == payload.exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    # Validasi input
    if payload.order is None or payload.order < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must be >= 0")
    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required")

    level = Level(
        id=uuid.uuid4(),
        exercise_id=payload.exercise_id,
        order=payload.order,
        title=payload.title.strip(),
        desc=payload.desc,
    )
    db.add(level)
    db.flush()
    return level


def update_level(db: Session, level_id: str, payload: LevelUpdate) -> Optional[Level]:
    level = get_level_by_id(db, level_id)
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    if payload.exercise_id is not None:
        exercise = db.query(Exercise).filter(Exercise.id == payload.exercise_id).first()
        if not exercise:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
        level.exercise_id = payload.exercise_id
    if payload.order is not None:
        if payload.order < 0:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Order must be >= 0")
        level.order = payload.order
    if payload.title is not None:
        if not payload.title.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty")
        level.title = payload.title.strip()
    if payload.desc is not None:
        level.desc = payload.desc
    db.flush()
    return level


def delete_level(db: Session, level_id: str) -> bool:
    level = get_level_by_id(db, level_id)
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    db.delete(level)
    return True