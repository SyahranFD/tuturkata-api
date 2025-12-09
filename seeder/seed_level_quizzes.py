import uuid
from typing import Dict, Tuple
from sqlalchemy.orm import Session

from app.model.level_quiz import LevelQuiz
from app.model.level import Level
from app.model.exercise import Exercise

def seed_level_quizzes(db: Session, levels_by_key: Dict[Tuple[str, int], Level]) -> None:

    def compute_quiz_exp(level: Level) -> int:
        exercise = db.get(Exercise, level.exercise_id)
        return 10 * int(exercise.order)
    specs = [
        # Membaca Kata — instruksi tidak menyebut ulang kata (speech_text)
        ("Membaca Kata", 1, [
            {"speech_text": "pa", "instruction": "Ulangi suku kata ini 5 kali."},
            {"speech_text": "ba", "instruction": "Ulangi suku kata ini 5 kali."},
            {"speech_text": "ta", "instruction": "Ulangi suku kata ini 5 kali."},
            {"speech_text": "ka", "instruction": "Ulangi suku kata ini 5 kali."},
            {"speech_text": "pi", "instruction": "Ulangi suku kata ini 5 kali."},
        ]),
        ("Membaca Kata", 2, [
            {"speech_text": "batu", "instruction": "Eja suku kata ini menjadi ba-tu"},
            {"speech_text": "sapu", "instruction": "Eja suku kata ini menjadi sa-pu"},
            {"speech_text": "pintu", "instruction": "Eja suku kata ini menjadi pin-tu"},
            {"speech_text": "pohon", "instruction": "Eja suku kata ini menjadi po-hon"},
            {"speech_text": "kamar", "instruction": "Eja suku kata ini menjadi ka-mar"},
        ]),
        ("Membaca Kata", 3, [
            {"speech_text": "makan", "instruction": "Ucapkan kata ini dengan tempo lambat dan jelas."},
            {"speech_text": "minum", "instruction": "Ucapkan kata ini dengan tempo lambat dan jelas."},
            {"speech_text": "tidur", "instruction": "Ucapkan kata ini dengan tempo lambat dan jelas."},
            {"speech_text": "buku", "instruction": "Ucapkan kata ini dengan tempo lambat dan jelas."},
            {"speech_text": "rumah", "instruction": "Ucapkan kata ini dengan tempo lambat dan jelas."},
        ]),
        ("Membaca Kata", 4, [
            {"speech_text": "perpustakaan", "instruction": "Artikulasi lembut untuk kata panjang; jaga ritme."},
            {"speech_text": "keterampilan", "instruction": "Fokus pada kejelasan tiap suku kata panjang."},
            {"speech_text": "kebudayaan", "instruction": "Pertahankan konsistensi tempo sepanjang kata."},
            {"speech_text": "operator", "instruction": "Ucapkan stabil, hindari jeda tak perlu."},
            {"speech_text": "berlomba", "instruction": "Jaga aliran suara dan transisi suku kata."},
        ]),
        ("Membaca Kata", 5, [
            {"speech_text": "infrastruktur", "instruction": "Latih konsonan gabung/diftong; jaga kelancaran."},
            {"speech_text": "psikologis", "instruction": "Fokus pada cluster konsonan yang menantang."},
            {"speech_text": "transkripsi", "instruction": "Pertahankan artikulasi pada konsonan beruntun."},
            {"speech_text": "konseptual", "instruction": "Jaga kejelasan suku kata yang kompleks."},
            {"speech_text": "pertanggungjawaban", "instruction": "Ucapkan perlahan; pecah suku kata bila perlu."},
        ]),

        # Kalimat Tingkat Dasar — instruksi per quiz disertakan
        ("Kalimat Tingkat Dasar", 1, [
            {"speech_text": "Saya suka kopi.", "instruction": "Baca kalimat berikut dengan tempo lambat dan jelas."},
            {"speech_text": "Ini buku saya.", "instruction": "Baca kalimat berikut dengan tempo lambat dan jelas."},
            {"speech_text": "Cuaca hari ini cerah.", "instruction": "Baca kalimat berikut dengan tempo lambat dan jelas."},
            {"speech_text": "Kucing itu lucu.", "instruction": "Baca kalimat berikut dengan tempo lambat dan jelas."},
            {"speech_text": "Dia pergi ke sekolah.", "instruction": "Baca kalimat berikut dengan tempo lambat dan jelas."},
        ]),
        ("Kalimat Tingkat Dasar", 2, [
            {"speech_text": "Halo.", "instruction": "Ulangi 3 kali mengikuti ritme yang sama."},
            {"speech_text": "Nama saya [nama].", "instruction": "Ucapkan 3 kali, fokus kejelasan pengucapan."},
            {"speech_text": "Senang bertemu denganmu.", "instruction": "Ulangi 3 kali dengan nada sopan."},
            {"speech_text": "Saya tinggal di [kota].", "instruction": "Ulangi 3 kali, jaga jeda antar frasa saat mengulang."},
            {"speech_text": "Umur saya [umur].", "instruction": "Ucapkan 3 kali, konsistenkan tempo."},
        ]),
        ("Kalimat Tingkat Dasar", 3, [
            {"speech_text": "Halo.", "instruction": "Ucapkan seperti sapaan awal, intonasi ramah."},
            {"speech_text": "Nama saya [nama].", "instruction": "Perkenalkan diri dengan tempo tenang."},
            {"speech_text": "Senang berkenalan.", "instruction": "Nada positif, artikulasi bersih."},
            {"speech_text": "Saya dari [kota].", "instruction": "Jeda singkat setelah subjek."},
            {"speech_text": "Sampai jumpa.", "instruction": "Penutup dengan intonasi menurun."},
        ]),
        ("Kalimat Tingkat Dasar", 4, [
            {"speech_text": "Hari ini saya belajar berbicara dengan perlahan agar suara lebih jelas.", "instruction": "Baca kalimat panjang dengan jeda di koma/titik."},
            {"speech_text": "Saya mencoba mengatur napas dan jeda saat mengucapkan kalimat panjang.", "instruction": "Jaga napas; berhenti singkat di frasa."},
            {"speech_text": "Dengan latihan teratur, pengucapan saya menjadi semakin stabil setiap hari.", "instruction": "Pertahankan ritme stabil sepanjang kalimat."},
            {"speech_text": "Saya percaya ketenangan membantu otak merencanakan suara dengan lebih baik.", "instruction": "Nada tenang, fokus kejelasan."},
            {"speech_text": "Mari terus berlatih agar komunikasi kita semakin lancar dan percaya diri.", "instruction": "Jeda alami, penutup tegas."},
        ]),
        ("Kalimat Tingkat Dasar", 5, [
            {"speech_text": "Hobi saya membaca.", "instruction": "Jawab singkat, artikulasi jelas."},
            {"speech_text": "Makanan favorit saya nasi goreng.", "instruction": "Jaga penekanan kata kunci."},
            {"speech_text": "Pekerjaan saya [profesi].", "instruction": "Ucapkan tegas dan pelan."},
            {"speech_text": "Saya lahir di [kota].", "instruction": "Nada informatif, ritme wajar."},
            {"speech_text": "Saya suka berolahraga.", "instruction": "Tuturan stabil, akhir kalimat turun."},
        ]),

        # Kalimat Tingkat Menengah
        ("Kalimat Tingkat Menengah", 1, [
            {"speech_text": "Setiap pagi saya berjalan di taman sambil mendengarkan musik. Udara segar membantu saya memulai hari dengan semangat.", "instruction": "Baca ~30 detik; jaga ritme stabil."},
            {"speech_text": "Membaca buku adalah kebiasaan yang saya jaga. Dari buku, saya belajar cara melihat dunia dari sudut berbeda.", "instruction": "Jeda wajar di tiap titik/komas."},
            {"speech_text": "Saya suka memasak makanan sederhana untuk keluarga. Kami biasanya makan bersama sambil bercerita tentang kegiatan hari ini.", "instruction": "Nada naratif, aliran tenang."},
            {"speech_text": "Perjalanan singkat ke pantai minggu lalu sangat menyenangkan. Suara ombak membuat saya merasa tenang.", "instruction": "Pertahankan kejelasan di frasa panjang."},
            {"speech_text": "Saya sedang mencoba rutin menulis jurnal. Kegiatan ini membantu saya memahami perasaan dan pikiran sendiri.", "instruction": "Tuturan stabil; jeda di frasa."},
        ]),
        ("Kalimat Tingkat Menengah", 2, [
            {"speech_text": "Selamat pagi, ada yang bisa saya bantu?", "instruction": "Roleplay: giliran 1 (menyapa)."},
            {"speech_text": "Saya mencari buku tentang sejarah.", "instruction": "Roleplay: giliran 2 (menyatakan kebutuhan)."},
            {"speech_text": "Berapa harganya?", "instruction": "Roleplay: giliran 3 (bertanya)."},
            {"speech_text": "Baik, saya ambil satu.", "instruction": "Roleplay: giliran 4 (keputusan)."},
            {"speech_text": "Terima kasih.", "instruction": "Roleplay: giliran 5 (penutup)."},
        ]),
        ("Kalimat Tingkat Menengah", 3, [
            {"speech_text": "Halo, saya ingin memesan satu porsi nasi goreng.", "instruction": "Telepon: buka pesanan dengan sopan."},
            {"speech_text": "Apakah bisa dikirimkan pukul tujuh?", "instruction": "Telepon: ajukan waktu pengantaran."},
            {"speech_text": "Alamat saya di Jalan Melati nomor lima.", "instruction": "Telepon: sebutkan alamat jelas."},
            {"speech_text": "Pembayarannya tunai saat tiba.", "instruction": "Telepon: sampaikan metode bayar."},
            {"speech_text": "Terima kasih, saya tunggu.", "instruction": "Telepon: tutup percakapan dengan sopan."},
        ]),
        ("Kalimat Tingkat Menengah", 4, [
            {"speech_text": "Saya melihat sebuah taman dengan pohon hijau dan bangku.", "instruction": "Deskripsi: sebutkan objek utama."},
            {"speech_text": "Ada seorang anak bermain bola di lapangan kecil.", "instruction": "Deskripsi: fokus aktivitas."},
            {"speech_text": "Langit cerah dengan beberapa awan putih tipis.", "instruction": "Deskripsi: kondisi cuaca."},
            {"speech_text": "Di sudut, terdapat kios kecil yang menjual minuman.", "instruction": "Deskripsi: detail lokasi."},
            {"speech_text": "Suasana tampak tenang dan nyaman untuk berjalan.", "instruction": "Deskripsi: simpulan suasana."},
        ]),
        ("Kalimat Tingkat Menengah", 5, [
            {"speech_text": "Kemarin saya menghadiri seminar teknologi yang menarik.", "instruction": "Ceritakan pengalaman (awal)."},
            {"speech_text": "Saya bertemu teman lama dan berbincang cukup lama.", "instruction": "Lanjutkan kronologi (pertengahan)."},
            {"speech_text": "Setelah itu kami makan malam di restoran dekat kampus.", "instruction": "Tambahkan detail kegiatan."},
            {"speech_text": "Perjalanan pulang sedikit macet tetapi saya tetap menikmati musik.", "instruction": "Sisipkan kondisi perjalanan."},
            {"speech_text": "Saya merasa hari itu produktif dan menyenangkan.", "instruction": "Tutup dengan kesan akhir."},
        ]),

        # Kalimat Tingkat Lanjut
        ("Kalimat Tingkat Lanjut", 1, [
            {"speech_text": "Saya ingin berbicara tentang pentingnya waktu berkualitas.", "instruction": "Monolog: buka topik inti."},
            {"speech_text": "Topik saya hari ini adalah kebiasaan membaca.", "instruction": "Monolog: sebutkan tema dengan jelas."},
            {"speech_text": "Saya akan menceritakan pengalaman belajar bahasa.", "instruction": "Monolog: jelaskan konteks pengalaman."},
            {"speech_text": "Saya ingin membahas manfaat olahraga rutin.", "instruction": "Monolog: paparkan poin utama."},
            {"speech_text": "Mari berbicara tentang teknologi dalam pendidikan.", "instruction": "Monolog: arahkan ke subtopik lain."},
        ]),
        ("Kalimat Tingkat Lanjut", 2, [
            {"speech_text": "Maaf, di mana kantor pos terdekat?", "instruction": "Skenario: bertanya arah (sopan)."},
            {"speech_text": "Terima kasih, tetapi saya tidak bisa menerima tawaran itu.", "instruction": "Skenario: menolak dengan sopan."},
            {"speech_text": "Mohon perhatian, saya akan berbicara di depan kelompok.", "instruction": "Skenario: mengawali pidato singkat."},
            {"speech_text": "Bisakah Anda menunjukkan arah ke stasiun?", "instruction": "Skenario: minta bantuan arah."},
            {"speech_text": "Saya perlu menolak undangan karena ada urusan keluarga.", "instruction": "Skenario: menolak undangan (alasan jelas)."},
        ]),
        ("Kalimat Tingkat Lanjut", 3, [
            {"speech_text": "Pembuka: tujuan presentasi saya adalah mengenalkan produk baru.", "instruction": "Presentasi: buka tujuan."},
            {"speech_text": "Bagian inti: keunggulan utama produk adalah kemudahan penggunaan.", "instruction": "Presentasi: sampaikan poin inti."},
            {"speech_text": "Contoh: pengguna dapat menyelesaikan tugas hanya dalam tiga langkah.", "instruction": "Presentasi: berikan contoh jelas."},
            {"speech_text": "Dampak: efisiensi meningkat dan waktu kerja berkurang.", "instruction": "Presentasi: jelaskan dampak."},
            {"speech_text": "Penutup: mari kita coba dan beri umpan balik.", "instruction": "Presentasi: tutup dan ajak audiens."},
        ]),
        ("Kalimat Tingkat Lanjut", 4, [
            {"speech_text": "Apakah harga ini masih bisa dinegosiasikan?", "instruction": "Negosiasi: ajukan pertanyaan awal."},
            {"speech_text": "Bagaimana jika kita sepakat di angka tengah?", "instruction": "Negosiasi: tawarkan kompromi."},
            {"speech_text": "Kami bisa menambah nilai dengan layanan purna jual.", "instruction": "Negosiasi: berikan nilai tambah."},
            {"speech_text": "Batas waktu kami adalah minggu depan, apakah memungkinkan?", "instruction": "Negosiasi: sampaikan batas waktu."},
            {"speech_text": "Jika setuju, mari kita buat perjanjian tertulis.", "instruction": "Negosiasi: ajak menyepakati akhir."},
        ]),
        ("Kalimat Tingkat Lanjut", 5, [
            {"speech_text": "Saya setuju bahwa pekerjaan jarak jauh meningkatkan produktivitas.", "instruction": "Debat: paparkan argumen pro."},
            {"speech_text": "Namun, interaksi langsung tetap penting untuk kerja tim.", "instruction": "Debat: sampaikan kontra/nuansa."},
            {"speech_text": "Dari sisi biaya, perusahaan menghemat ruang kantor.", "instruction": "Debat: berikan alasan pendukung."},
            {"speech_text": "Di sisi lain, kolaborasi bisa terhambat tanpa tatap muka.", "instruction": "Debat: paparkan kelemahan."},
            {"speech_text": "Kesimpulannya, kebijakan hybrid adalah pilihan yang seimbang.", "instruction": "Debat: simpulkan secara seimbang."},
        ]),
    ]

    for ex_title, order, quizzes in specs:
        level = levels_by_key.get((ex_title, order))
        if not level:
            continue
        for idx, item in enumerate(quizzes, start=1):
            speech_text = item["speech_text"]
            exists = (
                db.query(LevelQuiz)
                .filter(LevelQuiz.level_id == level.id, LevelQuiz.speech_text == speech_text)
                .first()
            )
            if exists:
                continue
            quiz = LevelQuiz(
                id=uuid.uuid4(),
                level_id=level.id,
                order=idx,
                instruction=item["instruction"],
                speech_text=item["speech_text"],
                exp=compute_quiz_exp(level),
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