import uuid
from sqlalchemy.orm import Session

from app.model.daily_mission import DailyMission


def seed_daily_missions(db: Session) -> None:
    samples = [
        {"title": "Selesaikan 3 latihan", "type": "exercise", "max_progress": 3},
        {"title": "Dapatkan 6 bintang", "type": "star", "max_progress": 6},
        {"title": "Capai akurasi 80%", "type": "accuration", "max_progress": 80},
    ]

    for s in samples:
        exists = db.query(DailyMission).filter(DailyMission.title == s["title"]).first()
        if exists:
            # keep max_progress up to date if changed
            if exists.max_progress != s["max_progress"]:
                exists.max_progress = s["max_progress"]
            continue
        mission = DailyMission(
            id=uuid.uuid4(),
            title=s["title"],
            type=s["type"],
            max_progress=s["max_progress"],
            current_progress=0,
            is_completed=False,
        )
        db.add(mission)


if __name__ == "__main__":
    from app.config.database import SessionLocal

    db = SessionLocal()
    try:
        seed_daily_missions(db)
        db.commit()
        print("Seed daily_missions selesai.")
    except Exception as e:
        db.rollback()
        print(f"Seed daily_missions gagal: {e}")
        raise
    finally:
        db.close()