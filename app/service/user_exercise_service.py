import uuid
from typing import List
from sqlalchemy.orm import Session

from ..model.user_exercise import UserExercise
from ..model.exercise import Exercise
from ..model.level import Level


def get_user_exercises_by_user_id(db: Session, user_id: str) -> List[dict]:
    # Join ke Exercise dan urutkan berdasarkan Exercise.order
    rows = (
        db.query(UserExercise, Exercise)
        .join(Exercise, Exercise.id == UserExercise.exercise_id)
        .filter(UserExercise.user_id == user_id)
        .order_by(Exercise.order.asc())
        .all()
    )

    if not rows:
        return []

    result = []
    for user_exercise, exercise in rows:
        result.append({
            "exercise_id": user_exercise.exercise_id,
            "max_level": user_exercise.max_level,
            "current_level": user_exercise.current_level,
            "title": exercise.title,
            "desc": exercise.desc,
        })

    return result


def upsert_current_level_by_exercise(db: Session, user_id: str, exercise_id: str, target_order: int) -> None:
    user_exercise = (
        db.query(UserExercise)
        .filter(UserExercise.user_id == user_id, UserExercise.exercise_id == exercise_id)
        .first()
    )
    if user_exercise:
        # Pastikan tidak menurunkan progress yang sudah lebih tinggi
        current = user_exercise.current_level or 0
        user_exercise.current_level = max(current, target_order)
    else:
        level_count = db.query(Level).filter(Level.exercise_id == exercise_id).count()
        new_ue = UserExercise(
            id=uuid.uuid4(),
            user_id=user_id,
            exercise_id=exercise_id,
            max_level=level_count,
            current_level=target_order,
        )
        db.add(new_ue)
    db.flush()