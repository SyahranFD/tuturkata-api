# Panduan Deploy TuturKata API (Tanpa Docker)

Dokumen ini menjelaskan langkah-langkah untuk mendeploy TuturKata API di VPS Linux menggunakan Gunicorn + Uvicorn dan Nginx, dengan struktur langkah mirip panduan yang pernah Anda buat sebelumnya.

## Prasyarat
- VPS Linux (Ubuntu/Debian direkomendasikan)
- Python 3.9+ terpasang
- PostgreSQL terpasang
- Nginx terpasang
- Git terpasang
- Domain (opsional, untuk HTTPS)

## 1) Persiapan VPS
Login ke VPS via SSH, lalu update sistem dan pasang dependensi:

```bash
ssh username@your_server_ip
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv postgresql postgresql-contrib nginx git
```

## 2) Konfigurasi PostgreSQL
Masuk ke PostgreSQL dan buat database serta user khusus untuk aplikasi:

```sql
sudo -u postgres psql

-- Buat database
CREATE DATABASE fastapi_tuturkata_api;

-- Buat user dan password aman
CREATE USER tuturkata WITH PASSWORD 'password_yang_aman';

-- Beri hak akses ke database
GRANT ALL PRIVILEGES ON DATABASE fastapi_tuturkata_api TO tuturkata;

-- Keluar dari PostgreSQL
\q
```

## 3) Clone Repository
Buat direktori aplikasi, ubah kepemilikan jika perlu, lalu clone repo:

```bash
sudo mkdir -p /var/www/tuturkata-api
sudo chown -R $USER:$USER /var/www/tuturkata-api
cd /var/www/tuturkata-api

# Clone repository (sesuaikan URL jika private)
git clone https://github.com/username/tuturkata-api.git .
```

## 4) Setup Python Environment
Buat virtual environment dan install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirement.txt
```

## 5) Konfigurasi Environment Variables
Buat file `.env` berdasarkan kebutuhan aplikasi ini.

```bash
cp .env.example .env  # jika tersedia, jika tidak buat manual
nano .env
```

Contoh isi `.env` yang relevan untuk proyek ini:

```env
# Database App (digunakan oleh SQLAlchemy di app/config/database.py)
DB_USER=tuturkata
DB_PASS=password_yang_aman
DB_NAME=fastapi_tuturkata_api
DB_HOST=localhost
DB_PORT=5432

# Pooling (opsional, gunakan default jika ragu)
DB_POOLSIZE=50
DB_MAXOVERFLOW=25
DB_POOLTIMEOUT=30
DB_POOLRECYCLE=1800

# JWT
SECRET_KEY=ganti_dengan_secret_yang_aman
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60

# Alembic membutuhkan URL eksplisit
SQLALCHEMY_DATABASE_URL=postgresql://tuturkata:password_yang_aman@localhost:5432/fastapi_tuturkata_api
```

Catatan:
- Aplikasi membaca DB_* dari `.env` untuk koneksi runtime.
- Alembic membaca `SQLALCHEMY_DATABASE_URL` dari `.env` saat migrasi (lihat `alembic/env.py`).

## 6) Jalankan Migrasi Database
Pastikan venv aktif, lalu jalankan migrasi Alembic:

```bash
source venv/bin/activate
alembic upgrade head
```

Opsional: Seed data awal jika diperlukan:

```bash
python -m seeder.seed_all
# atau jalankan seeder per modul, misal:
# python -m seeder.seed_users
# python -m seeder.seed_exercises
```

## 7) Konfigurasi Gunicorn + Systemd
Buat file service untuk Systemd:

```bash
sudo nano /etc/systemd/system/tuturkata-api.service
```

Isi dengan konfigurasi berikut:

```ini
[Unit]
Description=TuturKata API service
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/tuturkata-api
ExecStart=/var/www/tuturkata-api/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000
Restart=always
Environment="PATH=/var/www/tuturkata-api/venv/bin"
EnvironmentFile=/var/www/tuturkata-api/.env

[Install]
WantedBy=multi-user.target
```

Aktifkan dan jalankan service:

```bash
sudo systemctl enable tuturkata-api
sudo systemctl start tuturkata-api
sudo systemctl status tuturkata-api
```

> Jika port 8000 sudah terpakai, ganti `--bind 0.0.0.0:8000` ke port lain, dan sesuaikan konfigurasi Nginx pada langkah berikutnya.

## 8) Konfigurasi Nginx
Buat konfigurasi Nginx untuk reverse proxy ke Gunicorn:

```bash
sudo nano /etc/nginx/sites-available/tuturkata-api
```

Isi dengan konfigurasi berikut (sesuaikan `server_name` dengan domain Anda):

```nginx
server {
    listen 80;
    server_name domain-anda.com www.domain-anda.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Aktifkan konfigurasi dan restart Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/tuturkata-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

## 9) SSL dengan Certbot (Opsional)
Jika menggunakan domain publik, pasang sertifikat SSL:

```bash
sudo apt install -y certbot python3-certbot-nginx
sudo certbot --nginx -d domain-anda.com -d www.domain-anda.com
```

## Pemeliharaan & Update
### Update Aplikasi

```bash
cd /var/www/tuturkata-api
source venv/bin/activate
git pull
pip install -r requirement.txt
alembic upgrade head
sudo systemctl restart tuturkata-api
```

### Backup Database

```bash
sudo -u postgres pg_dump fastapi_tuturkata_api > backup_$(date +%Y%m%d).sql
```

### Melihat Log

```bash
# Log aplikasi (systemd)
sudo journalctl -u tuturkata-api -f

# Log Nginx
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

---

Catatan Tambahan:
- Di lingkungan Windows (dev), instalasi `psycopg2` bisa bermasalah; gunakan `psycopg2-binary` jika diperlukan. Di server Linux produksi, `psycopg2` standar direkomendasikan.
- Pastikan variabel `.env` disesuaikan dengan kredensial dan host database Anda.
- Aplikasi ini menggunakan waktu WIB (UTC+7) di sisi aplikasi untuk timestamp `created_at` dan `updated_at`, serta memformat tanggal keluaran JSON menjadi `YYYY-MM-DD` di skema respons.