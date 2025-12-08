import uuid
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app.model.level_quiz import LevelQuiz
from app.model.level import Level


def seed_level_quizzes(db: Session, levels_by_key: Dict[Tuple[str, int], Level]) -> None:
    # Untuk setiap level, buat maksimal 5 quiz.
    # Bagian "question" berisi kata/kalimat yang benar-benar harus diucapkan user.
    specs = [
        # Membaca Kata
        ("Membaca Kata", 1, "Baca kata sederhana secara perlahan", [
            "makan", "minum", "tidur", "buku", "rumah"
        ]),
        ("Membaca Kata", 2, "Ucapkan berulang huruf P, B, T, K", [
            "pa", "ba", "ta", "ka", "pi"
        ]),
        ("Membaca Kata", 3, "Baca kata berpola CV/CVC", [
            "batu", "sapu", "pintu", "tas", "kamar"
        ]),
        ("Membaca Kata", 4, "Artikulasi lembut tanpa tekanan", [
            "perjalanan", "kebersamaan", "kemungkinan", "telekomunikasi", "pengembangan"
        ]),
        ("Membaca Kata", 5, "Baca daftar kata acak", [
            "harmoni", "teknologi", "kebun", "lapangan", "keberanian"
        ]),

        # Kalimat Tingkat Dasar
        ("Kalimat Tingkat Dasar", 1, "Baca satu kalimat pendek", [
            "Saya suka kopi.", "Ini buku saya.", "Cuaca hari ini cerah.", "Kucing itu lucu.", "Dia pergi ke sekolah."
        ]),
        ("Kalimat Tingkat Dasar", 2, "Repeat-after-me kalimat pendek", [
            "Halo.", "Nama saya [nama].", "Senang bertemu denganmu.", "Saya tinggal di [kota].", "Umur saya [umur]."
        ]),
        ("Kalimat Tingkat Dasar", 3, "Percakapan sederhana perkenalan", [
            "Halo.", "Nama saya [nama].", "Senang berkenalan.", "Saya dari [kota].", "Sampai jumpa."
        ]),
        ("Kalimat Tingkat Dasar", 4, "Baca kalimat panjang", [
            "Hari ini saya belajar berbicara dengan perlahan agar suara lebih jelas.",
            "Saya mencoba mengatur napas dan jeda saat mengucapkan kalimat panjang.",
            "Dengan latihan teratur, pengucapan saya menjadi semakin stabil setiap hari.",
            "Saya percaya ketenangan membantu otak merencanakan suara dengan lebih baik.",
            "Mari terus berlatih agar komunikasi kita semakin lancar dan percaya diri."
        ]),
        ("Kalimat Tingkat Dasar", 5, "Tanya jawab sederhana", [
            "Hobi saya membaca.", "Makanan favorit saya nasi goreng.", "Pekerjaan saya [profesi].", "Saya lahir di [kota].", "Saya suka berolahraga."
        ]),

        # Kalimat Tingkat Menengah
        ("Kalimat Tingkat Menengah", 1, "Baca teks selama 30 detik", [
            "Setiap pagi saya berjalan di taman sambil mendengarkan musik. Udara segar membantu saya memulai hari dengan semangat.",
            "Membaca buku adalah kebiasaan yang saya jaga. Dari buku, saya belajar cara melihat dunia dari sudut berbeda.",
            "Saya suka memasak makanan sederhana untuk keluarga. Kami biasanya makan bersama sambil bercerita tentang kegiatan hari ini.",
            "Perjalanan singkat ke pantai minggu lalu sangat menyenangkan. Suara ombak membuat saya merasa tenang.",
            "Saya sedang mencoba rutin menulis jurnal. Kegiatan ini membantu saya memahami perasaan dan pikiran sendiri."
        ]),
        ("Kalimat Tingkat Menengah", 2, "Roleplay percakapan (3 giliran)", [
            "Selamat pagi, ada yang bisa saya bantu?",
            "Saya mencari buku tentang sejarah.",
            "Berapa harganya?",
            "Baik, saya ambil satu.",
            "Terima kasih."
        ]),
        ("Kalimat Tingkat Menengah", 3, "Simulasi telepon singkat", [
            "Halo, saya ingin memesan satu porsi nasi goreng.",
            "Apakah bisa dikirimkan pukul tujuh?",
            "Alamat saya di Jalan Melati nomor lima.",
            "Pembayarannya tunai saat tiba.",
            "Terima kasih, saya tunggu."
        ]),
        ("Kalimat Tingkat Menengah", 4, "Deskripsi gambar 30 detik", [
            "Saya melihat sebuah taman dengan pohon hijau dan bangku.",
            "Ada seorang anak bermain bola di lapangan kecil.",
            "Langit cerah dengan beberapa awan putih tipis.",
            "Di sudut, terdapat kios kecil yang menjual minuman.",
            "Suasana tampak tenang dan nyaman untuk berjalan."
        ]),
        ("Kalimat Tingkat Menengah", 5, "Ceritakan ulang pengalaman", [
            "Kemarin saya menghadiri seminar teknologi yang menarik.",
            "Saya bertemu teman lama dan berbincang cukup lama.",
            "Setelah itu kami makan malam di restoran dekat kampus.",
            "Perjalanan pulang sedikit macet tetapi saya tetap menikmati musik.",
            "Saya merasa hari itu produktif dan menyenangkan."
        ]),

        # Kalimat Tingkat Lanjut
        ("Kalimat Tingkat Lanjut", 1, "Percakapan bebas bertema 60 detik", [
            "Saya ingin berbicara tentang pentingnya waktu berkualitas.",
            "Topik saya hari ini adalah kebiasaan membaca.",
            "Saya akan menceritakan pengalaman belajar bahasa.",
            "Saya ingin membahas manfaat olahraga rutin.",
            "Mari berbicara tentang teknologi dalam pendidikan."
        ]),
        ("Kalimat Tingkat Lanjut", 2, "Percakapan di beberapa skenario", [
            "Maaf, di mana kantor pos terdekat?",
            "Terima kasih, tetapi saya tidak bisa menerima tawaran itu.",
            "Mohon perhatian, saya akan berbicara di depan kelompok.",
            "Bisakah Anda menunjukkan arah ke stasiun?",
            "Saya perlu menolak undangan karena ada urusan keluarga."
        ]),
        ("Kalimat Tingkat Lanjut", 3, "Presentasi singkat 90 detik", [
            "Pembuka: tujuan presentasi saya adalah mengenalkan produk baru.",
            "Bagian inti: keunggulan utama produk adalah kemudahan penggunaan.",
            "Contoh: pengguna dapat menyelesaikan tugas hanya dalam tiga langkah.",
            "Dampak: efisiensi meningkat dan waktu kerja berkurang.",
            "Penutup: mari kita coba dan beri umpan balik."
        ]),
        ("Kalimat Tingkat Lanjut", 4, "Negosiasi singkat", [
            "Apakah harga ini masih bisa dinegosiasikan?",
            "Bagaimana jika kita sepakat di angka tengah?",
            "Kami bisa menambah nilai dengan layanan purna jual.",
            "Batas waktu kami adalah minggu depan, apakah memungkinkan?",
            "Jika setuju, mari kita buat perjanjian tertulis."
        ]),
        ("Kalimat Tingkat Lanjut", 5, "Debat ringan", [
            "Saya setuju bahwa pekerjaan jarak jauh meningkatkan produktivitas.",
            "Namun, interaksi langsung tetap penting untuk kerja tim.",
            "Dari sisi biaya, perusahaan menghemat ruang kantor.",
            "Di sisi lain, kolaborasi bisa terhambat tanpa tatap muka.",
            "Kesimpulannya, kebijakan hybrid adalah pilihan yang seimbang."
        ]),
    ]

    for ex_title, order, instruction, questions in specs:
        level = levels_by_key.get((ex_title, order))
        if not level:
            continue
        for question in questions:
            exists = (
                db.query(LevelQuiz)
                .filter(LevelQuiz.level_id == level.id, LevelQuiz.question == question)
                .first()
            )
            if exists:
                continue
            quiz = LevelQuiz(
                id=uuid.uuid4(),
                level_id=level.id,
                instruction=instruction,
                question=question,
            )
            db.add(quiz)


if __name__ == "__main__":
    # Jalankan langsung untuk seed level quizzes saja
    from app.config.database import SessionLocal
    from .seed_exercises import seed_exercises
    from .seed_levels import seed_levels

    db = SessionLocal()
    try:
        exercises = seed_exercises(db)
        levels = seed_levels(db, exercises)
        seed_level_quizzes(db, levels)
        db.commit()
        print("Seed level quizzes selesai.")
    except Exception as e:
        db.rollback()
        print(f"Seed level quizzes gagal: {e}")
        raise
    finally:
        db.close()