from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.user_level import UserLevelCreate, UserLevelUpdate, UserLevelOut
from ..schemas.level import LevelWithCompletionOut
from ..service.user_level_service import (
    create_user_level,
    get_levels_completion_by_exercise,
)
from ..service.auth import get_current_user
from ..model.user import User


router_user_level = APIRouter(prefix="/api/user-levels", tags=["User Levels"])


@router_user_level.post("/", response_model=UserLevelOut, status_code=status.HTTP_201_CREATED)
def create_user_level_endpoint(payload: UserLevelCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    user_level = create_user_level(db, payload)
    return user_level

@router_user_level.get("/{exercise_id}", response_model=List[LevelWithCompletionOut])
def list_levels_completion_by_exercise(exercise_id: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_levels_completion_by_exercise(db, str(current_user.id), exercise_id)