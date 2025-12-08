import uuid
import random
from typing import List

from app.model.user import User
from app.model.level import Level
from app.model.user_level import UserLevel
from app.model.exercise import Exercise


def seed_user_levels(db) -> List[UserLevel]:
    created = []
    users = db.query(User).all()
    exercises = db.query(Exercise).all()
    # Untuk setiap exercise, pilih Level.order secara acak antara 1 sampai 3 per user
    for user in users:
        for exercise in exercises:
            random_order = random.randint(1, 3)
            for order in range(1, random_order + 1):
                level_for_order = (
                    db.query(Level)
                    .filter(Level.exercise_id == exercise.id, Level.order == order)
                    .first()
                )
                if not level_for_order:
                    continue
                exists = (
                    db.query(UserLevel)
                    .filter(UserLevel.user_id == user.id, UserLevel.level_id == level_for_order.id)
                    .first()
                )
                if exists:
                    continue
                user_level_entry = UserLevel(
                    id=uuid.uuid4(),
                    user_id=user.id,
                    level_id=level_for_order.id,
                    star=3,
                    accuration=100,
                )
                db.add(user_level_entry)
                created.append(user_level_entry)
    return created