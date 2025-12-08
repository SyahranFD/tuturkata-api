import uuid
import random
from typing import List

from app.model.user import User
from app.model.exercise import Exercise
from app.model.level import Level
from app.model.user_exercise import UserExercise


def seed_user_exercises(db) -> List[UserExercise]:
    created = []
    users = db.query(User).all()
    exercises = db.query(Exercise).all()
    for user in users:
        for ex in exercises:
            exists = (
                db.query(UserExercise)
                .filter(UserExercise.user_id == user.id, UserExercise.exercise_id == ex.id)
                .first()
            )
            if exists:
                continue
            level_count = db.query(Level).filter(Level.exercise_id == ex.id).count()
            # Pilih current_level secara acak antara 0 sampai level_count
            current_level_random = random.randint(0, level_count)

            user_exercise = UserExercise(
                id=uuid.uuid4(),
                user_id=user.id,
                exercise_id=ex.id,
                max_level=level_count,
                current_level=current_level_random,
            )
            db.add(user_exercise)
            created.append(user_exercise)
    return created