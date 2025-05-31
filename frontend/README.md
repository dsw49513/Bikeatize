🚴‍♂️ Bikeatize
Bikeatize to aplikacja webowa dla entuzjastów jazdy na rowerze. Pozwala:

śledzić trasy i lokalizację użytkownika,

gromadzić punkty za pokonany dystans,

zarządzać użytkownikami,

wizualizować pozycję na mapie,

analizować historię aktywności.

🗂️ Struktura projektu
bash
Copy
Edit
Bikeatize/
├── backend/                      # Backend FastAPI + SQLAlchemy
│   ├── auth.py                  # Logika JWT, logowanie, rejestracja
│   ├── main.py                  # Główna aplikacja FastAPI
│   ├── database/                # Połączenie z bazą danych
│   │   ├── database.py
│   │   ├── models.py
│   └── routes/                  # Endpointy REST API
│       ├── bt_points.py         # System punktów
│       ├── distance.py          # Obliczanie dystansu (Haversine)
│       ├── geolocation.py       # Zapis i odczyt lokalizacji
│       ├── trips.py             # Start/Stop trasy, zapis punktów
│       └── users.py             # CRUD użytkowników
├── frontend/                    # Frontend React + Vite
│   ├── src/
│   │   ├── context/             # AuthContext – globalna autoryzacja
│   │   ├── pages/               # Widoki aplikacji
│   │   │   ├── LoginPage.jsx
│   │   │   ├── RegisterPage.jsx
│   │   │   ├── Dashboard.jsx    # Mapa, punkty, dystans
│   │   │   └── HomePage.jsx
│   ├── public/
│   └── package.json             # Zależności React
├── .env                         # Sekrety backendu (JWT, DB)
├── requirements.txt             # Zależności backendu (FastAPI, etc.)
└── README.md
🔧 Wymagania
Python 3.10+

Node.js (frontend)

MySQL 8 (baza danych)

Docker (opcjonalnie do uruchomienia bazy)

⚙️ Uruchomienie projektu
1. Uruchomienie bazy danych (Docker):
bash
Copy
Edit
docker run --name biketize-db \
  -e MYSQL_ROOT_PASSWORD=secret \
  -e MYSQL_DATABASE=bikeatize \
  -p 3306:3306 \
  -d mysql:8
2. Backend (FastAPI):
bash
Copy
Edit
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r ../requirements.txt
uvicorn main:app --reload
3. Frontend (React):
bash
Copy
Edit
cd frontend
npm install
npm run dev
4. Zmienne środowiskowe (.env)
W katalogu głównym projektu 
```Bikeatize/.env
DATABASE_URL=mysql+aiomysql://user:haslo@localhost:3306/bikeatize_db
ALEMBIC_URL=mysql+pymysql://user:haslo@localhost:3306/bikeatize_db

SECRET_KEY=supersekretnyklucz123
```
W folderze frontend
```Bikeatize/frontend/.env
VITE_OPENWEATHER_API_KEY=klucz https://home.openweathermap.org/api_keys
```
🔐 Backend – najważniejsze endpointy
Metoda	Endpoint	Opis
POST	/api/register	Rejestracja użytkownika
POST	/api/login	Logowanie, JWT w odpowiedzi
GET	/bt_points/me	Pobranie punktów i dystansu (JWT)
POST	/start_trip/{user_id}	Rozpoczęcie nowej trasy
POST	/update_location/{trip_id}	Zapisanie lokalizacji trasy
POST	/stop_trip/{trip_id}	Zakończenie trasy i przyznanie punktów
GET	/trip_history/{user_id}	Historia tras

💡 Frontend – opis działania
LoginPage – loguje użytkownika, zapisuje token do AuthContext, przekierowuje do /dashboard

RegisterPage – tworzy konto i przekierowuje do logowania

Dashboard – pobiera punkty i dystans z backendu, wyświetla mapę z lokalizacją użytkownika

HomePage – strona główna, linki do logowania/rejestracji

🗺️ Mapa i lokalizacja
Używamy:

react-leaflet

leaflet