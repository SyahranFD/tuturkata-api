from app.config.database import SessionLocal
from .seed_users import seed_users
from .seed_exercises import seed_exercises
from .seed_levels import seed_levels
from .seed_level_quizzes import seed_level_quizzes


def run() -> None:
    db = SessionLocal()
    try:
        seed_users(db)
        exercises = seed_exercises(db)
        levels = seed_levels(db, exercises)
        seed_level_quizzes(db, levels)
        db.commit()
        print("Seeding selesai: users, exercises, levels, level_quizzes.")
    except Exception as e:
        db.rollback()
        print(f"Seeding gagal: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    run()