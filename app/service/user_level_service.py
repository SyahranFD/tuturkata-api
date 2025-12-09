import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..model.user_level import UserLevel
from ..model.user import User
from ..model.level import Level
from ..model.user_exercise import UserExercise
from ..model.exercise import Exercise
from ..schemas.user_level import UserLevelCreate, UserLevelUpdate


def create_user_level(db: Session, payload: UserLevelCreate) -> UserLevel:
    # Validate user and level
    user = db.query(User).filter(User.id == str(payload.user_id)).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    level = db.query(Level).filter(Level.id == str(payload.level_id)).first()
    if not level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Level not found")

    # Validate input
    if payload.star is None or payload.star < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Star must be >= 0")
    if payload.accuration is None or payload.accuration < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Accuration must be >= 0")
    if payload.exp is None or payload.exp < 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Exp must be >= 0")

    # find existing user level
    existing = (
        db.query(UserLevel)
        .filter(UserLevel.user_id == str(payload.user_id), UserLevel.level_id == str(payload.level_id))
        .first()
    )
    if existing:
        # Jika sudah ada, update nilai star dan accuration
        user_level = existing
        user_level.star = payload.star
        user_level.accuration = payload.accuration
    else:
        # Jika belum ada, buat baru
        user_level = UserLevel(
            id=uuid.uuid4(),
            user_id=str(payload.user_id),
            level_id=str(payload.level_id),
            star=payload.star,
            accuration=payload.accuration,
        )
        db.add(user_level)
        # Tambahkan exp ke user hanya saat create baru
        user.exp = (user.exp or 0) + payload.exp
    db.flush()

    # Update user_exercise.current_level if it exists
    user_exercise = (
        db.query(UserExercise)
        .filter(
            UserExercise.user_id == user.id,
            UserExercise.exercise_id == level.exercise_id,
        )
        .first()
    )
    if user_exercise:
        user_exercise.current_level = level.order
    else:
        # Jika belum ada, buat baru
        level_count = db.query(Level).filter(Level.exercise_id == level.exercise_id).count()
        user_exercise = UserExercise(
            id=uuid.uuid4(),
            user_id=user.id,
            exercise_id=level.exercise_id,
            max_level=level_count,
            current_level=level.order,
        )
        db.add(user_exercise)
    db.flush()
    return user_level


def get_levels_completion_by_exercise(db: Session, user_id: str, exercise_id: str):
    # Pastikan user dan exercise valid
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    # Ambil semua level untuk exercise tersebut, urutkan berdasarkan order
    levels = (
        db.query(Level)
        .filter(Level.exercise_id == exercise_id)
        .order_by(Level.order.asc())
        .all()
    )

    level_ids = [lvl.id for lvl in levels]

    # Ambil level yang sudah diselesaikan oleh user
    user_levels = (
        db.query(UserLevel)
        .filter(UserLevel.user_id == user_id, UserLevel.level_id.in_(level_ids))
        .all()
    )
    completed_ids = {ul.level_id for ul in user_levels}

    # Bangun output dengan flag isCompleted
    result = [
        {
            "level_id": lvl.id,
            "order": lvl.order,
            "title": lvl.title,
            "desc": getattr(lvl, "desc", None),
            "isCompleted": lvl.id in completed_ids,
        }
        for lvl in levels
    ]

    return result