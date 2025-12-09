import uuid
from typing import Dict
from sqlalchemy.orm import Session

from app.model.exercise import Exercise


def seed_exercises(db: Session) -> Dict[str, Exercise]:
    samples = [
        {
            "order": 1,
            "title": "Membaca Kata",
            "desc": "Latihan pengucapan kata dasar",
        },
        {
            "order": 2,
            "title": "Kalimat Tingkat Dasar",
            "desc": "Latihan pengucapan kalimat dasar",
        },
        {
            "order": 3,
            "title": "Kalimat Tingkat Menengah",
            "desc": "Latihan pengucapan kalimat menengah",
        },
        {
            "order": 4,
            "title": "Kalimat Tingkat Lanjut",
            "desc": "Latihan pengucapan kalimat lanjut",
        },
    ]

    by_title: Dict[str, Exercise] = {}

    for s in samples:
        exists = db.query(Exercise).filter(Exercise.title == s["title"]).first()
        if exists:
            # Pastikan order sesuai spesifikasi seed agar perhitungan EXP benar
            if exists.order != s["order"]:
                exists.order = s["order"]
            by_title[s["title"]] = exists
            continue
        exercise = Exercise(
            id=uuid.uuid4(),
            order=s["order"],
            title=s["title"],
            desc=s.get("desc"),
        )
        db.add(exercise)
        by_title[s["title"]] = exercise

    return by_title


if __name__ == "__main__":
    # Jalankan langsung untuk seed exercise saja
    from app.config.database import SessionLocal

    db = SessionLocal()
    try:
        seed_exercises(db)
        db.commit()
        print("Seed exercises selesai.")
    except Exception as e:
        db.rollback()
        print(f"Seed exercises gagal: {e}")
        raise
    finally:
        db.close()