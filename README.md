# 🚴‍♂️ Bikeatize

**Bikeatize** to aplikacja webowa dla entuzjastów jazdy na rowerze. Pozwala:

- śledzić trasy i lokalizację użytkownika w czasie rzeczywistym,
- gromadzić punkty za pokonany dystans,
- zarządzać użytkownikami (rejestracja/logowanie),
- wizualizować aktualną pozycję na mapie,
- analizować historię aktywności i usuwać trasy.

---

## 🗂️ Struktura projektu

```
Bikeatize/
├── alembic/                        # Pliki migracji (jeśli używasz Alembic)
│   ├── versions/
│   ├── env.py                      # Konfiguracja środowiska migracji
│   └── script.py.mako              # Szablon migracji
├── backend/
│   ├── core/
│   │   └── security.py             # Obsługa JWT, haszowanie haseł
│   ├── routes/                     # Endpointy FastAPI
│   │   ├── auth.py                 # Rejestracja i logowanie
│   │   ├── bt_points.py            # Zwrot punktów i dystansu (JWT)
│   │   ├── distance.py             # Obliczanie dystansu (Haversine)
│   │   ├── geolocation.py          # Obsługa lokalizacji
│   │   ├── trips.py                # Trasy: start, stop, historia
│   │   ├── users.py                # Operacje CRUD na użytkownikach
│   │   └── api_router.py           # Łączenie routerów
│   ├── main.py                     # FastAPI app
├── database/
│   ├── database.py                 # Połączenie i sesje bazy danych
│   └── models.py                   # Modele SQLAlchemy (User, Trip, itp.)
├── schemas/
│   ├── user.py                     # Schematy użytkownika (Pydantic)
│   ├── location.py                 # Schematy lokalizacji (Pydantic)
│   └── __init__.py
├── frontend/
│   ├── public/                     # Pliki publiczne dla Vite
│   └── src/
│       ├── api/                    # Komunikacja z backendem
│       │   ├── authApi.js
│       │   ├── tripAPI.js
│       │   └── userApi.js
│       ├── components/            # Komponenty UI
│       │   ├── RideTracker.jsx    # Śledzenie trasy rowerowej
│       │   ├── TripsHistory.jsx   # Historia tras i usuwanie
│       │   ├── UserForm.jsx
│       │   └── UserList.jsx
│       ├── context/
│       │   └── AuthContext.jsx    # Globalna autoryzacja + userId
│       ├── pages/                 # Widoki stron
│       │   ├── Dashboard.jsx      # Główna strona użytkownika
│       │   ├── LoginPage.jsx
│       │   ├── RegisterPage.jsx
│       │   └── HomePage.jsx
│       ├── App.jsx
│       ├── main.jsx
│       └── index.js
├── .env                            # Sekrety backendu (JWT, DB)
├── README.md
├── requirements.txt                # Zależności backendu
├── package.json                    # Zależności frontendowe
└── vite.config.js                  # Konfiguracja Vite
```

---

## 🔧 Wymagania

- Python 3.10+
- Node.js (frontend)
- MySQL 8 (baza danych)
- Docker (opcjonalnie do uruchomienia bazy)

---

## ⚙️ Uruchomienie projektu

### 1. Baza danych (Docker):

```bash
docker run --name biketize-db \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=bikeatize \
  -p 3306:3306 \
  -d mysql:8
```

### 2. Backend (FastAPI):

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
uvicorn main:app --reload
```

### 3. Frontend (React):

```bash
cd frontend
npm install
npm run dev
```
### 4. Zmienne środowiskowe (.env)
W katalogu głównym projektu 
```Bikeatize/.env
DATABASE_URL=mysql+aiomysql://user:haslo@localhost:3306/bikeatize_db
ALEMBIC_URL=mysql+pymysql://user:haslo@localhost:3306/bikeatize_db

SECRET_KEY=supersekretnyklucz123
```
W folderze frontend
```Bikeatize/frontend/.env
VITE_OPENWEATHER_API_KEY=twój klucz https://home.openweathermap.org/api_keys
VITE_API_URL=https://twoj-backend.pl/api
```
---

## 🔐 Backend – najważniejsze endpointy

| Metoda | Endpoint                            | Opis                                       |
|--------|-------------------------------------|--------------------------------------------|
| POST   | `/api/register`                     | Rejestracja użytkownika                    |
| POST   | `/api/login`                        | Logowanie, JWT w odpowiedzi                |
| GET    | `/api/bt_points/me`                 | Punkty i całkowity dystans (JWT)          |
| POST   | `/api/trips/start_trip/{user_id}`   | Rozpoczęcie nowej trasy                    |
| POST   | `/api/trips/update_location/{id}`   | Zapisanie lokalizacji trasy                |
| POST   | `/api/trips/stop_trip/{trip_id}`    | Zakończenie trasy i przyznanie punktów     |
| GET    | `/api/trips/trip_history/{user_id}` | Historia tras użytkownika                  |
| DELETE | `/api/trips/delete/{trip_id}`       | Usunięcie trasy                            |
| GET    | `/api/trips/total_distance/{id}`    | Całkowity dystans użytkownika              |

---

## 💡 Frontend – opis działania

- **LoginPage** – loguje użytkownika, zapisuje token w `AuthContext`, dekoduje `userId`, przekierowuje do dashboardu.
- **RegisterPage** – rejestruje użytkownika i przekierowuje do logowania.
- **Dashboard** – pobiera dane użytkownika, wyświetla mapę, uruchamia `RideTracker`, pokazuje `TripsHistory`, obsługuje usuwanie tras.
- **TripsHistory** – lista wszystkich tras z przyciskiem "Usuń".
- **RideTracker** – umożliwia rozpoczęcie/zakończenie trasy i śledzi lokalizację co 5 sekund.
- **HomePage** – prosty landing page z nawigacją.

---

## 🗺️ Mapa i lokalizacja

- Używamy **React Leaflet + Leaflet**
- Geolokalizacja z `navigator.geolocation`
- Dane tras zapisywane cyklicznie w `trip_locations`