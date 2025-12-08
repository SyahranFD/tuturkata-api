import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..model.exercise import Exercise
from ..schemas.exercise import ExerciseCreate, ExerciseUpdate


def get_exercise_by_id(db: Session, exercise_id: str) -> Optional[Exercise]:
    return db.query(Exercise).filter(Exercise.id == exercise_id).first()


def get_all_exercises(db: Session) -> List[Exercise]:
    return db.query(Exercise).order_by(Exercise.title.asc()).all()


def create_exercise(db: Session, payload: ExerciseCreate) -> Exercise:
    if not payload.title or not payload.title.strip():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title is required")
    exercise = Exercise(
        id=uuid.uuid4(),
        title=payload.title.strip(),
        desc=payload.desc,
    )
    db.add(exercise)
    db.flush()
    return exercise


def update_exercise(db: Session, exercise_id: str, payload: ExerciseUpdate) -> Optional[Exercise]:
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    if payload.title is not None:
        if not payload.title.strip():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Title cannot be empty")
        exercise.title = payload.title.strip()
    if payload.desc is not None:
        exercise.desc = payload.desc
    db.flush()
    return exercise


def delete_exercise(db: Session, exercise_id: str) -> bool:
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    db.delete(exercise)
    return True