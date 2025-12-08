import uuid
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app.model.level_quiz import LevelQuiz
from app.model.level import Level


def seed_level_quizzes(db: Session, levels_by_key: Dict[Tuple[str, int], Level]) -> None:
    # Untuk setiap level, buat maksimal 5 quiz.
    # Bagian "question" berisi kata/kalimat yang benar-benar harus diucapkan user.
    # Instruksi kini disimpan di dalam daftar specs per quiz (tidak dipisah fungsi).
    specs = [
        # Membaca Kata — instruksi tidak menyebut ulang kata (question)
        ("Membaca Kata", 1, [
            {"question": "makan", "instruction": "Ucapkan dengan tempo lambat dan jelas."},
            {"question": "minum", "instruction": "Jeda antar suku kata bila perlu."},
            {"question": "tidur", "instruction": "Fokus pada artikulasi vokal yang bersih."},
            {"question": "buku", "instruction": "Nada tenang, ritme stabil."},
            {"question": "rumah", "instruction": "Ucapkan sekali, lalu ulangi dengan tempo sama."},
        ]),
        ("Membaca Kata", 2, [
            {"question": "pa", "instruction": "Ulangi suku kata ini 5 kali dengan artikulasi lembut."},
            {"question": "ba", "instruction": "Jaga bibir/lidah tidak menekan berlebihan."},
            {"question": "ta", "instruction": "Pertahankan jeda yang konsisten antar pengulangan."},
            {"question": "ka", "instruction": "Jaga aliran napas tetap stabil."},
            {"question": "pi", "instruction": "Ucapkan 5 kali dengan intensitas suara ringan."},
        ]),
        ("Membaca Kata", 3, [
            {"question": "batu", "instruction": "Pecah menjadi suku kata, lalu ucapkan dengan jelas."},
            {"question": "sapu", "instruction": "Eja per suku kata sebelum mengucapkan."},
            {"question": "pintu", "instruction": "Jaga transisi antar suku kata tetap halus."},
            {"question": "tas", "instruction": "Tempo tenang, hindari tekanan berlebih."},
            {"question": "kamar", "instruction": "Ucapkan per suku kata lalu satukan utuh."},
        ]),
        ("Membaca Kata", 4, [
            {"question": "perpustakaan", "instruction": "Artikulasi lembut untuk kata panjang; jaga ritme."},
            {"question": "keterampilan", "instruction": "Fokus pada kejelasan tiap suku kata panjang."},
            {"question": "kebudayaan", "instruction": "Pertahankan konsistensi tempo sepanjang kata."},
            {"question": "operator", "instruction": "Ucapkan stabil, hindari jeda tak perlu."},
            {"question": "berlomba", "instruction": "Jaga aliran suara dan transisi suku kata."},
        ]),
        ("Membaca Kata", 5, [
            {"question": "infrastruktur", "instruction": "Latih konsonan gabung/diftong; jaga kelancaran."},
            {"question": "psikologis", "instruction": "Fokus pada cluster konsonan yang menantang."},
            {"question": "transkripsi", "instruction": "Pertahankan artikulasi pada konsonan beruntun."},
            {"question": "konseptual", "instruction": "Jaga kejelasan suku kata yang kompleks."},
            {"question": "pertanggungjawaban", "instruction": "Ucapkan perlahan; pecah suku kata bila perlu."},
        ]),

        # Kalimat Tingkat Dasar — instruksi per quiz disertakan
        ("Kalimat Tingkat Dasar", 1, [
            {"question": "Saya suka kopi.", "instruction": "Baca kalimat pendek dengan intonasi tenang."},
            {"question": "Ini buku saya.", "instruction": "Jaga kejelasan tiap kata dan jeda alami."},
            {"question": "Cuaca hari ini cerah.", "instruction": "Ucapkan stabil, hindari terburu-buru."},
            {"question": "Kucing itu lucu.", "instruction": "Nada ramah, artikulasi jelas."},
            {"question": "Dia pergi ke sekolah.", "instruction": "Jaga ritme dan penekanan kata penting."},
        ]),
        ("Kalimat Tingkat Dasar", 2, [
            {"question": "Halo.", "instruction": "Ulangi 3 kali mengikuti ritme yang sama."},
            {"question": "Nama saya [nama].", "instruction": "Ucapkan 3 kali, fokus kejelasan pengucapan."},
            {"question": "Senang bertemu denganmu.", "instruction": "Ulangi 3 kali dengan nada sopan."},
            {"question": "Saya tinggal di [kota].", "instruction": "Jaga jeda antar frasa saat mengulang."},
            {"question": "Umur saya [umur].", "instruction": "Ucapkan 3 kali, konsistenkan tempo."},
        ]),
        ("Kalimat Tingkat Dasar", 3, [
            {"question": "Halo.", "instruction": "Ucapkan seperti sapaan awal, intonasi ramah."},
            {"question": "Nama saya [nama].", "instruction": "Perkenalkan diri dengan tempo tenang."},
            {"question": "Senang berkenalan.", "instruction": "Nada positif, artikulasi bersih."},
            {"question": "Saya dari [kota].", "instruction": "Jeda singkat setelah subjek."},
            {"question": "Sampai jumpa.", "instruction": "Penutup dengan intonasi menurun."},
        ]),
        ("Kalimat Tingkat Dasar", 4, [
            {"question": "Hari ini saya belajar berbicara dengan perlahan agar suara lebih jelas.", "instruction": "Baca kalimat panjang dengan jeda di koma/titik."},
            {"question": "Saya mencoba mengatur napas dan jeda saat mengucapkan kalimat panjang.", "instruction": "Jaga napas; berhenti singkat di frasa."},
            {"question": "Dengan latihan teratur, pengucapan saya menjadi semakin stabil setiap hari.", "instruction": "Pertahankan ritme stabil sepanjang kalimat."},
            {"question": "Saya percaya ketenangan membantu otak merencanakan suara dengan lebih baik.", "instruction": "Nada tenang, fokus kejelasan."},
            {"question": "Mari terus berlatih agar komunikasi kita semakin lancar dan percaya diri.", "instruction": "Jeda alami, penutup tegas."},
        ]),
        ("Kalimat Tingkat Dasar", 5, [
            {"question": "Hobi saya membaca.", "instruction": "Jawab singkat, artikulasi jelas."},
            {"question": "Makanan favorit saya nasi goreng.", "instruction": "Jaga penekanan kata kunci."},
            {"question": "Pekerjaan saya [profesi].", "instruction": "Ucapkan tegas dan pelan."},
            {"question": "Saya lahir di [kota].", "instruction": "Nada informatif, ritme wajar."},
            {"question": "Saya suka berolahraga.", "instruction": "Tuturan stabil, akhir kalimat turun."},
        ]),

        # Kalimat Tingkat Menengah
        ("Kalimat Tingkat Menengah", 1, [
            {"question": "Setiap pagi saya berjalan di taman sambil mendengarkan musik. Udara segar membantu saya memulai hari dengan semangat.", "instruction": "Baca ~30 detik; jaga ritme stabil."},
            {"question": "Membaca buku adalah kebiasaan yang saya jaga. Dari buku, saya belajar cara melihat dunia dari sudut berbeda.", "instruction": "Jeda wajar di tiap titik/komas."},
            {"question": "Saya suka memasak makanan sederhana untuk keluarga. Kami biasanya makan bersama sambil bercerita tentang kegiatan hari ini.", "instruction": "Nada naratif, aliran tenang."},
            {"question": "Perjalanan singkat ke pantai minggu lalu sangat menyenangkan. Suara ombak membuat saya merasa tenang.", "instruction": "Pertahankan kejelasan di frasa panjang."},
            {"question": "Saya sedang mencoba rutin menulis jurnal. Kegiatan ini membantu saya memahami perasaan dan pikiran sendiri.", "instruction": "Tuturan stabil; jeda di frasa."},
        ]),
        ("Kalimat Tingkat Menengah", 2, [
            {"question": "Selamat pagi, ada yang bisa saya bantu?", "instruction": "Roleplay: giliran 1 (menyapa)."},
            {"question": "Saya mencari buku tentang sejarah.", "instruction": "Roleplay: giliran 2 (menyatakan kebutuhan)."},
            {"question": "Berapa harganya?", "instruction": "Roleplay: giliran 3 (bertanya)."},
            {"question": "Baik, saya ambil satu.", "instruction": "Roleplay: giliran 4 (keputusan)."},
            {"question": "Terima kasih.", "instruction": "Roleplay: giliran 5 (penutup)."},
        ]),
        ("Kalimat Tingkat Menengah", 3, [
            {"question": "Halo, saya ingin memesan satu porsi nasi goreng.", "instruction": "Telepon: buka pesanan dengan sopan."},
            {"question": "Apakah bisa dikirimkan pukul tujuh?", "instruction": "Telepon: ajukan waktu pengantaran."},
            {"question": "Alamat saya di Jalan Melati nomor lima.", "instruction": "Telepon: sebutkan alamat jelas."},
            {"question": "Pembayarannya tunai saat tiba.", "instruction": "Telepon: sampaikan metode bayar."},
            {"question": "Terima kasih, saya tunggu.", "instruction": "Telepon: tutup percakapan dengan sopan."},
        ]),
        ("Kalimat Tingkat Menengah", 4, [
            {"question": "Saya melihat sebuah taman dengan pohon hijau dan bangku.", "instruction": "Deskripsi: sebutkan objek utama."},
            {"question": "Ada seorang anak bermain bola di lapangan kecil.", "instruction": "Deskripsi: fokus aktivitas."},
            {"question": "Langit cerah dengan beberapa awan putih tipis.", "instruction": "Deskripsi: kondisi cuaca."},
            {"question": "Di sudut, terdapat kios kecil yang menjual minuman.", "instruction": "Deskripsi: detail lokasi."},
            {"question": "Suasana tampak tenang dan nyaman untuk berjalan.", "instruction": "Deskripsi: simpulan suasana."},
        ]),
        ("Kalimat Tingkat Menengah", 5, [
            {"question": "Kemarin saya menghadiri seminar teknologi yang menarik.", "instruction": "Ceritakan pengalaman (awal)."},
            {"question": "Saya bertemu teman lama dan berbincang cukup lama.", "instruction": "Lanjutkan kronologi (pertengahan)."},
            {"question": "Setelah itu kami makan malam di restoran dekat kampus.", "instruction": "Tambahkan detail kegiatan."},
            {"question": "Perjalanan pulang sedikit macet tetapi saya tetap menikmati musik.", "instruction": "Sisipkan kondisi perjalanan."},
            {"question": "Saya merasa hari itu produktif dan menyenangkan.", "instruction": "Tutup dengan kesan akhir."},
        ]),

        # Kalimat Tingkat Lanjut
        ("Kalimat Tingkat Lanjut", 1, [
            {"question": "Saya ingin berbicara tentang pentingnya waktu berkualitas.", "instruction": "Monolog: buka topik inti."},
            {"question": "Topik saya hari ini adalah kebiasaan membaca.", "instruction": "Monolog: sebutkan tema dengan jelas."},
            {"question": "Saya akan menceritakan pengalaman belajar bahasa.", "instruction": "Monolog: jelaskan konteks pengalaman."},
            {"question": "Saya ingin membahas manfaat olahraga rutin.", "instruction": "Monolog: paparkan poin utama."},
            {"question": "Mari berbicara tentang teknologi dalam pendidikan.", "instruction": "Monolog: arahkan ke subtopik lain."},
        ]),
        ("Kalimat Tingkat Lanjut", 2, [
            {"question": "Maaf, di mana kantor pos terdekat?", "instruction": "Skenario: bertanya arah (sopan)."},
            {"question": "Terima kasih, tetapi saya tidak bisa menerima tawaran itu.", "instruction": "Skenario: menolak dengan sopan."},
            {"question": "Mohon perhatian, saya akan berbicara di depan kelompok.", "instruction": "Skenario: mengawali pidato singkat."},
            {"question": "Bisakah Anda menunjukkan arah ke stasiun?", "instruction": "Skenario: minta bantuan arah."},
            {"question": "Saya perlu menolak undangan karena ada urusan keluarga.", "instruction": "Skenario: menolak undangan (alasan jelas)."},
        ]),
        ("Kalimat Tingkat Lanjut", 3, [
            {"question": "Pembuka: tujuan presentasi saya adalah mengenalkan produk baru.", "instruction": "Presentasi: buka tujuan."},
            {"question": "Bagian inti: keunggulan utama produk adalah kemudahan penggunaan.", "instruction": "Presentasi: sampaikan poin inti."},
            {"question": "Contoh: pengguna dapat menyelesaikan tugas hanya dalam tiga langkah.", "instruction": "Presentasi: berikan contoh jelas."},
            {"question": "Dampak: efisiensi meningkat dan waktu kerja berkurang.", "instruction": "Presentasi: jelaskan dampak."},
            {"question": "Penutup: mari kita coba dan beri umpan balik.", "instruction": "Presentasi: tutup dan ajak audiens."},
        ]),
        ("Kalimat Tingkat Lanjut", 4, [
            {"question": "Apakah harga ini masih bisa dinegosiasikan?", "instruction": "Negosiasi: ajukan pertanyaan awal."},
            {"question": "Bagaimana jika kita sepakat di angka tengah?", "instruction": "Negosiasi: tawarkan kompromi."},
            {"question": "Kami bisa menambah nilai dengan layanan purna jual.", "instruction": "Negosiasi: berikan nilai tambah."},
            {"question": "Batas waktu kami adalah minggu depan, apakah memungkinkan?", "instruction": "Negosiasi: sampaikan batas waktu."},
            {"question": "Jika setuju, mari kita buat perjanjian tertulis.", "instruction": "Negosiasi: ajak menyepakati akhir."},
        ]),
        ("Kalimat Tingkat Lanjut", 5, [
            {"question": "Saya setuju bahwa pekerjaan jarak jauh meningkatkan produktivitas.", "instruction": "Debat: paparkan argumen pro."},
            {"question": "Namun, interaksi langsung tetap penting untuk kerja tim.", "instruction": "Debat: sampaikan kontra/nuansa."},
            {"question": "Dari sisi biaya, perusahaan menghemat ruang kantor.", "instruction": "Debat: berikan alasan pendukung."},
            {"question": "Di sisi lain, kolaborasi bisa terhambat tanpa tatap muka.", "instruction": "Debat: paparkan kelemahan."},
            {"question": "Kesimpulannya, kebijakan hybrid adalah pilihan yang seimbang.", "instruction": "Debat: simpulkan secara seimbang."},
        ]),
    ]

    for ex_title, order, quizzes in specs:
        level = levels_by_key.get((ex_title, order))
        if not level:
            continue
        for idx, item in enumerate(quizzes, start=1):
            question = item["question"]
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
                order=idx,
                instruction=item["instruction"],
                question=item["question"],
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