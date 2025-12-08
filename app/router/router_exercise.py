from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.exercise import ExerciseCreate, ExerciseUpdate, ExerciseOut
from ..service.exercise_service import (
    create_exercise,
    get_exercise_by_id,
    get_all_exercises,
    update_exercise,
    delete_exercise,
)
from ..service.auth import get_current_user
from ..model.user import User


router_exercise = APIRouter(prefix="/api/exercises", tags=["Exercises"])


@router_exercise.post("/", response_model=ExerciseOut, status_code=status.HTTP_201_CREATED)
def create_exercise_endpoint(payload: ExerciseCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    exercise = create_exercise(db, payload)
    return exercise


@router_exercise.get("/", response_model=List[ExerciseOut])
def list_exercises(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_all_exercises(db)


@router_exercise.get("/{exercise_id}", response_model=ExerciseOut)
def read_exercise(exercise_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    exercise = get_exercise_by_id(db, exercise_id)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise


@router_exercise.put("/{exercise_id}", response_model=ExerciseOut)
def update_exercise_endpoint(exercise_id: str, payload: ExerciseUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    exercise = update_exercise(db, exercise_id, payload)
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return exercise


@router_exercise.delete("/{exercise_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_exercise_endpoint(exercise_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    deleted = delete_exercise(db, exercise_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")
    return None