import uuid
from typing import Dict
from sqlalchemy.orm import Session

from app.model.badge import Badge
from app.model.exercise import Exercise
from app.model.user import User


def seed_badges(db: Session, exercises_by_title: Dict[str, Exercise]) -> None:
    # Find default user to attach badges to
    user = db.query(User).filter(User.email == "andi@gmail.com").first()
    if not user:
        user = db.query(User).first()
    if not user:
        raise RuntimeError("No user found to attach badges. Seed users first.")

    samples_normal = [
        ("Master Kata", "Selesaikan semua level tingkat kata", "book_laurel", "normal", "Membaca Kata"),
        ("Master Kalimat Dasar", "Selesaikan semua level tingkat kalimat dasar", "book_laurel_1_star", "normal", "Kalimat Tingkat Dasar"),
        ("Master Kalimat Menengah", "Selesaikan semua level tingkat kalimat menengah", "book_laurel_2_star", "normal", "Kalimat Tingkat Menengah"),
        ("Master Kalimat Lanjut", "Selesaikan semua level tingkat kalimat lanjut", "book_laurel_crown", "normal", "Kalimat Tingkat Lanjut"),
    ]

    samples_endless = [
        ("Endless Pemula", "Selesaikan 10 latihan di Endless", "endless_laurel", "endless"),
        ("Endless Terampil", "Selesaikan 25 latihan di Endless", "endless_laurel_1_star", "endless"),
        ("Endless Mahir", "Selesaikan 50 latihan di Endless", "endless_laurel_2_star", "endless"),
        ("Endless Master", "Selesaikan 75 latihan di Endless", "endless_laurel_3_star", "endless"),
        ("Endless Legend", "Selesaikan 100 latihan di Endless", "endless_laurel_crown", "endless"),
    ]

    # Seed normal badges (with exercise_id mapped by title)
    for title, desc, icon_name, btype, exercise_title in samples_normal:
        exists = db.query(Badge).filter(Badge.title == title, Badge.user_id == user.id).first()
        if exists:
            # keep icon/type/desc updated if changed
            if exists.icon_name != icon_name:
                exists.icon_name = icon_name
            if exists.type != btype:
                exists.type = btype
            if exists.desc != desc:
                exists.desc = desc
            continue
        ex = exercises_by_title.get(exercise_title)
        if not ex:
            ex = db.query(Exercise).filter(Exercise.title == exercise_title).first()
        badge = Badge(
            id=uuid.uuid4(),
            user_id=user.id,
            exercise_id=getattr(ex, "id", None),
            title=title,
            icon_name=icon_name,
            desc=desc,
            type=btype,
            is_completed=False,
        )
        db.add(badge)

    # Seed endless badges (no exercise_id)
    for title, desc, icon_name, btype in samples_endless:
        exists = db.query(Badge).filter(Badge.title == title, Badge.user_id == user.id).first()
        if exists:
            if exists.icon_name != icon_name:
                exists.icon_name = icon_name
            if exists.type != btype:
                exists.type = btype
            if exists.desc != desc:
                exists.desc = desc
            continue
        badge = Badge(
            id=uuid.uuid4(),
            user_id=user.id,
            exercise_id=None,
            title=title,
            icon_name=icon_name,
            desc=desc,
            type=btype,
            is_completed=False,
        )
        db.add(badge)


if __name__ == "__main__":
    from app.config.database import SessionLocal
    from .seed_exercises import seed_exercises

    db = SessionLocal()
    try:
        exercises = seed_exercises(db)
        seed_badges(db, exercises)
        db.commit()
        print("Seed badges selesai.")
    except Exception as e:
        db.rollback()
        print(f"Seed badges gagal: {e}")
        raise
    finally:
        db.close()