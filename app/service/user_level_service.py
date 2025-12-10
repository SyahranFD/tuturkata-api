import uuid
from typing import Optional, List
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from ..model.user_level import UserLevel
from ..model.user import User
from ..model.level import Level
from ..model.user_exercise import UserExercise
from ..service.user_exercise_service import upsert_current_level_by_exercise
from ..model.exercise import Exercise
from ..schemas.user_level import UserLevelCreate, UserLevelUpdate


def create_user_level(db: Session, payload: UserLevelCreate, current_user: User) -> UserLevel:
    # Validate user and level
    user = db.query(User).filter(User.id == str(current_user.id)).first()
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
        .filter(UserLevel.user_id == str(current_user.id), UserLevel.level_id == str(payload.level_id))
        .first()
    )
    if existing:
        # Jika sudah ada, update nilai star dan accuration
        user_level = existing
        user_level.star = payload.star
        user_level.accuration = payload.accuration
        # Pastikan updated_at terbarui
        try:
            from ..utils.time import wib_now
            user_level.updated_at = wib_now()
        except Exception:
            pass
    else:
        # Jika belum ada, buat baru
        user_level = UserLevel(
            id=uuid.uuid4(),
            user_id=str(current_user.id),
            level_id=str(payload.level_id),
            star=payload.star,
            accuration=payload.accuration,
        )
        db.add(user_level)
        # Tambahkan exp ke user hanya saat create baru
        user.exp = (user.exp or 0) + payload.exp
    db.flush()

    # Update atau buat UserExercise current_level melalui service helper
    upsert_current_level_by_exercise(db, user.id, level.exercise_id, level.order)
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
    stats_by_level = {ul.level_id: {"star": ul.star, "accuration": ul.accuration, "updated_at": ul.updated_at} for ul in user_levels}

    # Bangun output dengan flag isCompleted
    result = [
        {
            "level_id": lvl.id,
            "order": lvl.order,
            "title": lvl.title,
            "desc": getattr(lvl, "desc", None),
            "star": stats_by_level.get(lvl.id, {}).get("star", 0),
            "accuration": stats_by_level.get(lvl.id, {}).get("accuration", 0),
            "updated_at": stats_by_level.get(lvl.id, {}).get("updated_at", None),
            "isCompleted": lvl.id in completed_ids,
        }
        for lvl in levels
    ]

    return result


def get_next_level_for_exercise(db: Session, user_id: str, exercise_id: str):
    # Validate user and exercise
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Exercise not found")

    # Find latest updated level for this exercise
    latest_level = (
        db.query(Level)
        .join(UserLevel, UserLevel.level_id == Level.id)
        .filter(UserLevel.user_id == user_id, Level.exercise_id == exercise_id)
        .order_by(UserLevel.updated_at.desc())
        .first()
    )

    # Determine next order: first level if no progress yet
    next_order = (latest_level.order + 1) if latest_level else 1

    # Fetch next level by order
    next_level = (
        db.query(Level)
        .filter(Level.exercise_id == exercise_id, Level.order == next_order)
        .first()
    )

    if not next_level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Next level not found")

    return {"level_id": next_level.id, "title": next_level.title}


def get_next_level_for_user(db: Session, user_id: str):
    # Cari progress terbaru user di semua exercise
    latest_level = (
        db.query(Level)
        .join(UserLevel, UserLevel.level_id == Level.id)
        .filter(UserLevel.user_id == user_id)
        .order_by(UserLevel.updated_at.desc())
        .first()
    )

    if latest_level:
        # Tentukan level berikutnya dalam exercise yang sama
        next_order = latest_level.order + 1
        next_level = (
            db.query(Level)
            .filter(Level.exercise_id == latest_level.exercise_id, Level.order == next_order)
            .first()
        )
        if not next_level:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Next level not found")
        return {"exercise_id": next_level.exercise_id, "level_id": next_level.id, "title": next_level.title}

    # Jika belum ada progress: ambil exercise pertama lalu level pertama
    first_exercise = db.query(Exercise).order_by(Exercise.order.asc()).first()
    if not first_exercise:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No exercises available")

    first_level = (
        db.query(Level)
        .filter(Level.exercise_id == first_exercise.id)
        .order_by(Level.order.asc())
        .first()
    )
    if not first_level:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No levels available for the first exercise")

    return {"exercise_id": first_level.exercise_id, "level_id": first_level.id, "title": first_level.title}