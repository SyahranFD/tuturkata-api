from typing import List
from sqlalchemy.orm import Session

from ..model.user_exercise import UserExercise
from ..model.exercise import Exercise


def get_user_exercises_by_user_id(db: Session, user_id: str) -> List[dict]:
    user_exercise_list = (
        db.query(UserExercise)
        .filter(UserExercise.user_id == user_id)
        .all()
    )

    if not user_exercise_list:
        return []

    exercise_id_list = [user_exercise.exercise_id for user_exercise in user_exercise_list]
    exercise_list = db.query(Exercise).filter(Exercise.id.in_(exercise_id_list)).all()
    exercise_by_id = {exercise.id: exercise for exercise in exercise_list}

    result = []
    for user_exercise in user_exercise_list:
        exercise = exercise_by_id.get(user_exercise.exercise_id)
        result.append({
            "exercise_id": user_exercise.exercise_id,
            "max_level": user_exercise.max_level,
            "current_level": user_exercise.current_level,
            "title": exercise.title if exercise else None,
            "desc": exercise.desc if exercise else None,
        })

    return result