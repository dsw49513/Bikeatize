# 🚴 Bikeatize – Backend (FastAPI + MySQL)

Backend aplikacji do śledzenia aktywności rowerowej użytkowników.

## 🔧 Wymagania

- Python 3.10+
- MySQL lub MariaDB
- `pip` / `poetry` (do instalacji zależności)

## 🚀 Instalacja

1. **Sklonuj repozytorium**
```bash
git clone https://github.com/TwojeRepo/Bikeatize.git
cd Bikeatize/backend
```

2. **Stwórz wirtualne środowisko i zainstaluj zależności**
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Utwórz plik `.env`**
```env
SECRET_KEY=twoj_super_tajny_klucz
DATABASE_URL=mysql+asyncmy://user:password@localhost:3306/bikeatize_db
```

4. **Wykonaj migrację bazy danych**
```bash
alembic upgrade head
```

5. **Uruchom backend**
```bash
uvicorn backend.main:app --reload
```

Aplikacja będzie dostępna na: [http://127.0.0.1:8000](http://127.0.0.1:8000)

---

## 📚 API – Główne endpointy

### 🔐 Autoryzacja
- `POST /login` – logowanie
- `POST /register` – rejestracja
- `POST /logout` – wylogowanie
- `POST /refresh` – odświeżenie tokena

### 📍 Trasy rowerowe
- `POST /start_trip/{user_id}` – rozpoczęcie trasy
- `POST /update_location/{trip_id}?latitude=X&longitude=Y` – aktualizacja lokalizacji
- `POST /stop_trip/{trip_id}` – zakończenie trasy
- `GET /trip_history/{user_id}` – historia tras

---

## 🧠 Uwagi

- Plik `.env` musi znajdować się w katalogu `backend/`.
- Jeśli `asyncmy` nie działa na Pythonie 3.12+, możesz użyć `aiomysql`.
