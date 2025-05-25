# 🚲 Bikeatize

Aplikacja dla entuzjastów jazdy na rowerze, która łączy geolokalizację, analizę tras i motywacyjne systemy osiągnięć. Umożliwia użytkownikom:

- śledzenie swoich tras,
- zbieranie punktów,
- rywalizację w rankingach.

## ⚙️ Technologie

- 🌐 Geolocation API
- 🐍 FastAPI + Python
- ⚛️ ReactJS (wcześniej Angular/FastUI)
- 📱 Progressive Web App (PWA)
- 🔐 JWT Auth
- 🐬 MySQL (obecnie, wcześniej PostgreSQL)
- 🧵 SQLAlchemy (async ORM, `asyncmy`)

## 📦 Instalacja lokalna

### 1. Baza danych (MySQL przez Docker)
```bash
docker run --name biketize-db -e MYSQL_ROOT_PASSWORD=secret -e MYSQL_DATABASE=biketize_db -p 3306:3306 -d mysql:8
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
DATABASE_URL=mysql+asyncmy://root:secret@localhost:3306/biketize_db
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

Bikeatize/  
├─ .gitignore  
├─ alembic.ini  
├─ README.md           # opis projektu, instrukcje migration  
├─ requirements.txt    # zależności ogólne  
├─ alembic/            # skrypty migracji bazy danych  
│  ├─ env.py  
│  ├─ README  
│  └─ script.py.mako  
├─ backend/            # serwer FastAPI  
│  ├─ .dockerignore  
│  ├─ .gitignore  
│  ├─ README.md        # instrukcje uruchomienia backendu  
│  ├─ requirements.txt # zależności Pythona  
│  ├─ main.py          # instancja FastAPI + routery  
│  ├─ auth.py          # obsługa JWT, logowania/rejestracji  
│  ├─ models.py        # definicje ORM (SQLAlchemy async)  
│  ├─ schemas.py       # Pydantic-owe modele danych  
│  ├─ utils.py         # funkcje pomocnicze (np. haszowanie haseł)  
│  ├─ reset_users.py   # skrypt testowy do zerowania danych  
│  └─ core/security.py # konfiguracja bezpieczeństwa, klucze JWT  
└─ frontend/           # aplikacja React + Vite (PWA)  
   ├─ package.json  
   ├─ vite.config.js  
   ├─ public/         # manifest PWA, ikony  
   │  ├─ manifest.json  
   │  └─ icon-*.png  
   └─ src/  
      ├─ main.jsx      # punkt wejścia, ReactDOM.render  
      ├─ App.jsx       # routowanie do stron  
      ├─ api/          # wywołania do backendu (authApi.js, userApi.js)  
      ├─ components/   # formularze i listy (LoginForm, RegisterForm, UserList…)  
      └─ pages/        # strony: HomePage, LoginPage, RegisterPage  


## 🔁 API

| Endpoint       | Metoda | Opis                        |
|----------------|--------|-----------------------------|
| `/api/users`   | GET    | Pobiera listę użytkowników |
| `/api/users`   | POST   | Dodaje nowego użytkownika  |
