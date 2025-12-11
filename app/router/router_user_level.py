from fastapi import APIRouter, Depends, HTTPException, status
from uuid import UUID
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.user_level import UserLevelCreate, UserLevelUpdate, UserLevelOut
from ..schemas.level import LevelWithCompletionOut, LevelNextOut
from ..service.user_level_service import (
    create_user_level,
    get_levels_completion_by_exercise,
    get_next_level_for_exercise,
    get_next_level_for_user,
)
from ..service.auth import get_current_user
from ..model.user import User


router_user_level = APIRouter(prefix="/api/user-levels", tags=["User Levels"])


@router_user_level.post("/", response_model=UserLevelOut, status_code=status.HTTP_201_CREATED)
def create_user_level_endpoint(payload: UserLevelCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    user_level = create_user_level(db, payload, current_user)
    return user_level

@router_user_level.get("/next", response_model=LevelNextOut)
def get_next_level_endpoint(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_next_level_for_user(db, str(current_user.id))

@router_user_level.get("/{exercise_id}", response_model=List[LevelWithCompletionOut])
def list_levels_completion_by_exercise(exercise_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_levels_completion_by_exercise(db, str(current_user.id), str(exercise_id))