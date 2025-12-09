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

@router_level_quiz.get("/by-level/{level_id}", response_model=List[LevelQuizOut])
def list_level_quizzes_by_level(level_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_level_quizzes_by_level_id(db, level_id)