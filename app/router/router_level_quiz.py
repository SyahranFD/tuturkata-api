from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.level_quiz import LevelQuizCreate, LevelQuizUpdate, LevelQuizOut
from ..service.level_quiz_service import (
    create_level_quiz,
    get_level_quiz_by_id,
    get_all_level_quizzes,
    get_level_quizzes_by_level_id,
    update_level_quiz,
    delete_level_quiz,
)
from ..service.auth import get_current_user
from ..model.user import User


router_level_quiz = APIRouter(prefix="/api/level-quizzes", tags=["Level Quizzes"])


@router_level_quiz.post("/", response_model=LevelQuizOut, status_code=status.HTTP_201_CREATED)
def create_level_quiz_endpoint(payload: LevelQuizCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    level_quiz = create_level_quiz(db, payload)
    return level_quiz


@router_level_quiz.get("/", response_model=List[LevelQuizOut])
def list_level_quizzes(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_all_level_quizzes(db)


@router_level_quiz.get("/by-level/{level_id}", response_model=List[LevelQuizOut])
def list_level_quizzes_by_level(level_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_level_quizzes_by_level_id(db, level_id)


@router_level_quiz.get("/{level_quiz_id}", response_model=LevelQuizOut)
def read_level_quiz(level_quiz_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    level_quiz = get_level_quiz_by_id(db, level_quiz_id)
    if not level_quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level Quiz not found")
    return level_quiz


@router_level_quiz.put("/{level_quiz_id}", response_model=LevelQuizOut)
def update_level_quiz_endpoint(level_quiz_id: str, payload: LevelQuizUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    level_quiz = update_level_quiz(db, level_quiz_id, payload)
    if not level_quiz:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level Quiz not found")
    return level_quiz


@router_level_quiz.delete("/{level_quiz_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_level_quiz_endpoint(level_quiz_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    deleted = delete_level_quiz(db, level_quiz_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level Quiz not found")
    return None