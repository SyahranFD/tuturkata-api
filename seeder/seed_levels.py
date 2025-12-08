import uuid
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app.model.level import Level
from app.model.exercise import Exercise


def seed_levels(db: Session, exercises_by_title: Dict[str, Exercise]) -> Dict[Tuple[str, int], Level]:
    # Buat 5 level untuk setiap exercise, dengan judul dan deskripsi yang relevan
    specs = [
        # Membaca Kata
        ("Membaca Kata", 1, "Level 1 - Pemula", "Kata-kata sederhana"),
        ("Membaca Kata", 2, "Level 2 - Dasar", "Kata-kata umum"),
        ("Membaca Kata", 3, "Level 3 - Menengah", "Kata-kata pendek"),
        ("Membaca Kata", 4, "Level 4 - Lanjutan", "Kata-kata kompleks"),
        ("Membaca Kata", 5, "Level 5 - Mahir", "Kata-kata lengkap"),

        # Kalimat Tingkat Dasar
        ("Kalimat Tingkat Dasar", 1, "Level 1 - Pemula", "Kalimat sangat pendek"),
        ("Kalimat Tingkat Dasar", 2, "Level 2 - Dasar", "Kalimat umum sehari-hari"),
        ("Kalimat Tingkat Dasar", 3, "Level 3 - Menengah", "Kalimat gabungan sederhana"),
        ("Kalimat Tingkat Dasar", 4, "Level 4 - Lanjutan", "Kalimat panjang dasar"),
        ("Kalimat Tingkat Dasar", 5, "Level 5 - Mahir", "Kalimat kompleks ringan"),

        # Kalimat Tingkat Menengah
        ("Kalimat Tingkat Menengah", 1, "Level 1 - Pemula", "Paragraf pendek (3–4 kalimat)"),
        ("Kalimat Tingkat Menengah", 2, "Level 2 - Dasar", "Teks menengah ~15 detik"),
        ("Kalimat Tingkat Menengah", 3, "Level 3 - Menengah", "Teks ~30 detik"),
        ("Kalimat Tingkat Menengah", 4, "Level 4 - Lanjutan", "Dialog menengah"),
        ("Kalimat Tingkat Menengah", 5, "Level 5 - Mahir", "Monolog ~45 detik"),

        # Kalimat Tingkat Lanjut
        ("Kalimat Tingkat Lanjut", 1, "Level 1 - Pemula", "Tema bebas ~60 detik"),
        ("Kalimat Tingkat Lanjut", 2, "Level 2 - Dasar", "Skenario kompleks"),
        ("Kalimat Tingkat Lanjut", 3, "Level 3 - Menengah", "Presentasi singkat ~90 detik"),
        ("Kalimat Tingkat Lanjut", 4, "Level 4 - Lanjutan", "Negosiasi singkat"),
        ("Kalimat Tingkat Lanjut", 5, "Level 5 - Mahir", "Debat ringan"),
    ]

    by_key: Dict[Tuple[str, int], Level] = {}

    for ex_title, order, title, desc in specs:
        exercise = exercises_by_title.get(ex_title)
        if not exercise:
            continue
        exists = (
            db.query(Level)
            .filter(Level.exercise_id == exercise.id, Level.order == order)
            .first()
        )
        if exists:
            by_key[(ex_title, order)] = exists
            continue
        level = Level(
            id=uuid.uuid4(),
            exercise_id=exercise.id,
            order=order,
            title=title,
            desc=desc,
        )
        db.add(level)
        by_key[(ex_title, order)] = level

    return by_key


if __name__ == "__main__":
    # Jalankan langsung untuk seed levels saja
    from app.config.database import SessionLocal
    from .seed_exercises import seed_exercises

    db = SessionLocal()
    try:
        exercises = seed_exercises(db)
        seed_levels(db, exercises)
        db.commit()
        print("Seed levels selesai.")
    except Exception as e:
        db.rollback()
        print(f"Seed levels gagal: {e}")
        raise
    finally:
        db.close()