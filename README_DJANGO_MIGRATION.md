# HelloMind Django Upgrade

HelloMind sekarang memiliki fondasi Django + Django REST Framework yang modular, dengan endpoint kompatibel untuk frontend lama.

## Stack

- Django
- Django REST Framework
- SimpleJWT
- MySQL XAMPP via PyMySQL
- Groq API via OpenAI-compatible SDK
- django-cors-headers
- Celery + Redis optional

## Struktur

```text
config/
  settings.py
  urls.py
  celery.py
apps/
  authentication/
  chat/
  mood/
  emotion/
  persona/
  safety/
  dashboard/
  ai_services/
static/
  index.html
  login.html
  dashboard.html
  *.js, *.css
```

## Instalasi

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
```

Isi `.env` dengan `GROQ_API_KEY` dan konfigurasi MySQL XAMPP.

Pastikan MySQL XAMPP berjalan dan database sudah dibuat:

```sql
CREATE DATABASE hellomind CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

Lalu jalankan:

```powershell
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8000
```

## Cek Groq

Gunakan command ini setelah mengisi `.env`:

```powershell
python manage.py check_groq
```

Jika muncul `invalid_api_key`, buat API key Groq baru lalu ganti `GROQ_API_KEY` di `.env`.
Project memakai `GROQ_TRUST_ENV=False` secara default agar proxy environment lokal seperti `HTTP_PROXY=http://127.0.0.1:9` tidak ikut dipakai oleh request Groq.

## Endpoint Kompatibel Frontend Existing

- `POST /auth/register`
- `POST /auth/login`
- `GET /auth/me`
- `PUT /auth/settings`
- `GET /chats`
- `POST /chats`
- `PUT /chats/{chat_id}`
- `DELETE /chats/{chat_id}`
- `GET /chats/{chat_id}/messages`
- `POST /chat`
- `GET /mood/history?days=30`
- `GET /mood/summary?days=7`

Endpoint versi REST juga tersedia di prefix `api/v1`.

## Arsitektur

- `models.py`: hanya schema database dan relasi.
- `serializers.py`: validasi request dan format response.
- `views.py`: tipis, hanya HTTP orchestration.
- `services.py`: business logic utama.
- `apps/ai_services`: Groq client dan task Celery optional.
- `apps/safety`: safety policy, crisis handling, off-topic filter.
- `apps/emotion`: text emotion classifier.
- `apps/persona`: prompt builder, persona per bahasa, dan guardrail agar custom persona hanya mengubah gaya bicara tanpa mengganti peran inti HelloMind sebagai mental health companion.

## Strategi Migrasi Dari FastAPI

1. Jalankan Django di database baru atau database `hellomind` yang sama dengan table Django baru.
2. Migrasikan user ke `authentication_user`. Password legacy dari bcrypt custom sebaiknya di-reset atau di-import dengan password unusable, lalu pakai flow reset password.
3. Migrasikan `chats`, `messages`, dan `mood_entries` dengan mapping user lama ke user Django baru.
4. Pertahankan frontend lama karena route kompatibel sudah tersedia.
5. Setelah endpoint Django stabil, arsipkan file FastAPI lama (`main.py`, `auth.py`, `database.py`, `models.py`) atau pindahkan ke folder `legacy/`.

## Production Checklist

- Set `DJANGO_DEBUG=False`.
- Gunakan `DJANGO_SECRET_KEY` baru yang panjang dan rahasia.
- Isi `DJANGO_ALLOWED_HOSTS` sesuai domain.
- Set `CSRF_COOKIE_SECURE=True`, `SESSION_COOKIE_SECURE=True`, dan `SECURE_SSL_REDIRECT=True` saat memakai HTTPS.
- Simpan `.env` di server, jangan commit secret.
- Jalankan dengan Gunicorn/Uvicorn worker di belakang Nginx.
- Gunakan Redis jika mengaktifkan Celery.
- Tambahkan rate limiting untuk endpoint `/chat` sebelum public release.
