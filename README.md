# 🚲 Bikeatize

**Aplikacja dla entuzjastów jazdy na rowerze**, która łączy geolokalizację, analizę tras i motywacyjne systemy osiągnięć. Umożliwia użytkownikom:

- śledzenie swoich tras,
- zbieranie punktów,
- rywalizację w rankingach.

---

## ⚙️ Technologie

- 🌐 Geolocation API
- 🐍 FastAPI + Python
- ⚛️ ReactJS (wcześniej Angular/FastUI)
- 📱 Progressive Web App (PWA)
- 🔐 JWT Auth
- 🐘 PostgreSQL (obecnie, wcześniej MySQL)
- 🧵 SQLAlchemy (async ORM)

---

## 📦 Instalacja lokalna

### 1. Baza danych (PostgreSQL przez Docker)

```bash
docker run --name biketize-db -e POSTGRES_PASSWORD=secret -p 5432:5432 -d postgres
```

### 2. Backend (FastAPI)

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
```

Upewnij się, że masz plik `.env` w katalogu głównym projektu:

```env
DATABASE_URL=postgresql+asyncpg://postgres:secret@localhost:5432/postgres

DATABASE_URL=mysql+aiomysql://user:haslo@localhost:3306/bikeatize_db
ALEMBIC_URL=mysql+pymysql://user:haslo@localhost:3306/bikeatize_db

SECRET_KEY=supersekretnyklucz123
```

Uruchom serwer:
```bash
cd ..
PYTHONPATH=. uvicorn backend.main:app --reload
```

### 3. Frontend (React + Vite)

```bash
cd frontend
npm install
npm run dev
```

---

## 🔁 API

| Endpoint        | Metoda | Opis                     |
|-----------------|--------|--------------------------|
| `/api/users`    | GET    | Pobiera listę użytkowników |
| `/api/users`    | POST   | Dodaje nowego użytkownika |

---
