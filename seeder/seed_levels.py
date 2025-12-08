import uuid
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app.model.level import Level
from app.model.exercise import Exercise


def seed_levels(db: Session, exercises_by_title: Dict[str, Exercise]) -> Dict[Tuple[str, int], Level]:
    # Buat 5 level untuk setiap exercise, dengan judul dan deskripsi yang relevan
    specs = [
        # Membaca Kata
        ("Membaca Kata", 1, "Kata Sederhana (Tempo Lambat)", "Ucapkan kata dasar secara perlahan untuk melatih perencanaan suara."),
        ("Membaca Kata", 2, "Pengulangan Konsonan P/B/T/K", "Ucapkan suku kata P/B/T/K beberapa kali dengan artikulasi lembut."),
        ("Membaca Kata", 3, "Kata Berpola CV/CVC", "Eja kata berpola suku kata dan ucapkan per suku kata."),
        ("Membaca Kata", 4, "Kata Kompleks (Artikulasi Lembut)", "Latih kata lebih panjang tanpa tekanan bibir/lidah."),
        ("Membaca Kata", 5, "Daftar Kata Acak", "Jaga konsistensi lafal pada variasi kata acak."),

        # Kalimat Tingkat Dasar
        ("Kalimat Tingkat Dasar", 1, "Kalimat Pendek", "Baca satu kalimat pendek dengan intonasi tenang."),
        ("Kalimat Tingkat Dasar", 2, "Repeat After Me", "Ikuti dan ulangi kalimat pelatih untuk pola perkenalan sederhana."),
        ("Kalimat Tingkat Dasar", 3, "Dialog Perkenalan", "Roleplay sapaan dan perkenalan singkat."),
        ("Kalimat Tingkat Dasar", 4, "Kalimat Panjang", "Baca kalimat panjang 20–25 kata dengan jeda wajar."),
        ("Kalimat Tingkat Dasar", 5, "Tanya Jawab", "Jawab pertanyaan sederhana tentang diri Anda."),

        # Kalimat Tingkat Menengah
        ("Kalimat Tingkat Menengah", 1, "Teks 30 Detik", "Baca paragraf selama ~30 detik dengan ritme stabil."),
        ("Kalimat Tingkat Menengah", 2, "Roleplay 3 Giliran", "Percakapan bergantian tiga putaran (tanya–jawab–tindak lanjut)."),
        ("Kalimat Tingkat Menengah", 3, "Telepon Singkat", "Simulasi memesan atau membuat janji via telepon."),
        ("Kalimat Tingkat Menengah", 4, "Deskripsi Gambar", "Jelaskan gambar selama ~30 detik, fokus pada detail."),
        ("Kalimat Tingkat Menengah", 5, "Cerita Pengalaman", "Sampaikan pengalaman harian selama ~45 detik."),

        # Kalimat Tingkat Lanjut
        ("Kalimat Tingkat Lanjut", 1, "Tema Bebas 60 Detik", "Monolog topik pilihan selama ~60 detik."),
        ("Kalimat Tingkat Lanjut", 2, "Skenario Kompleks", "Bertanya arah, menolak permintaan, berbicara di depan kelompok."),
        ("Kalimat Tingkat Lanjut", 3, "Presentasi 90 Detik", "Struktur presentasi singkat: pembuka–isi–penutup."),
        ("Kalimat Tingkat Lanjut", 4, "Negosiasi Singkat", "Tawar-menawar atau menyepakati waktu/biaya."),
        ("Kalimat Tingkat Lanjut", 5, "Debat Ringan", "Argumen pro/kontra selama sekitar 120 detik."),
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