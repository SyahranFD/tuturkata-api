from app.config.database import SessionLocal
from .seed_users import seed_users
from .seed_exercises import seed_exercises
from .seed_levels import seed_levels
from .seed_level_quizzes import seed_level_quizzes
from .seed_user_exercises import seed_user_exercises
from .seed_user_levels import seed_user_levels
from .seed_daily_missions import seed_daily_missions
from .seed_badges import seed_badges


def run() -> None:
    db = SessionLocal()
    try:
        seed_users(db)
        exercises = seed_exercises(db)
        levels = seed_levels(db, exercises)

        db.commit()

        seed_level_quizzes(db, levels)
        seed_user_exercises(db)
        seed_user_levels(db)
        seed_daily_missions(db)
        seed_badges(db, exercises)

        db.commit()
        print("Seeding selesai: users, exercises, levels, level_quizzes, user_exercises, user_levels, daily_missions, badges.")
    except Exception as e:
        db.rollback()
        print(f"Seeding gagal: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()