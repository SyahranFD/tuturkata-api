from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.user_exercise import UserExerciseWithExerciseOut
from ..service.user_exercise_service import get_user_exercises_by_user_id
from ..service.auth import get_current_user
from ..model.user import User


router_user_exercise = APIRouter(prefix="/api/user-exercises", tags=["User Exercises"])


@router_user_exercise.get("/", response_model=List[UserExerciseWithExerciseOut])
def list_my_user_exercises(db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return get_user_exercises_by_user_id(db, str(current_user.id))