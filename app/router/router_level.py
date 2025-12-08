from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from ..config.database import get_db
from ..schemas.level import LevelCreate, LevelUpdate, LevelOut
from ..service.level_service import (
    create_level,
    get_level_by_id,
    get_all_levels,
    get_levels_by_exercise_id,
    update_level,
    delete_level,
)
from ..service.auth import get_current_user
from ..model.user import User


router_level = APIRouter(prefix="/api/levels", tags=["Levels"])


@router_level.post("/", response_model=LevelOut, status_code=status.HTTP_201_CREATED)
def create_level_endpoint(payload: LevelCreate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    level = create_level(db, payload)
    return level


@router_level.get("/", response_model=List[LevelOut])
def list_levels(db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_all_levels(db)


@router_level.get("/by-exercise/{exercise_id}", response_model=List[LevelOut])
def list_levels_by_exercise(exercise_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    return get_levels_by_exercise_id(db, exercise_id)


@router_level.get("/{level_id}", response_model=LevelOut)
def read_level(level_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    level = get_level_by_id(db, level_id)
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    return level


@router_level.put("/{level_id}", response_model=LevelOut)
def update_level_endpoint(level_id: str, payload: LevelUpdate, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    level = update_level(db, level_id, payload)
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    return level


@router_level.delete("/{level_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_level_endpoint(level_id: str, db: Session = Depends(get_db), _: User = Depends(get_current_user)):
    deleted = delete_level(db, level_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")
    return None