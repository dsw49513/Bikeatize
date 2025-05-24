from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Middleware CORS dla frontendu

# Import funkcji inicjalizującej bazę danych
from database.database import init_db
from backend.routes.geolocation import router as geolocation_router
from backend.auth import router as auth_router  # Router autoryzacji
from backend.routes.distance import router as distance_router
from backend.routes.trips import router as trips_router  # Endpointy do mierzenia trasy start stop

# Tworzenie aplikacji FastAPI
app = FastAPI()

# Otwarcie dostępu dla frontendu
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adres frontendu
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Wywołanie inicjalizacji bazy danych przy starcie serwera
@app.on_event("startup")
async def startup_event():
    await init_db()

# Rejestracja routerów
app.include_router(geolocation_router)  # Endpointy lokalizacji
app.include_router(auth_router)  # Endpointy związane z autoryzacją
app.include_router(distance_router)  # Endpointy do zliczania kilometrów
app.include_router(trips_router)  # Endpointy do mierzenia trasy start-stop

# Endpoint testowy, aby sprawdzić, czy API działa
@app.get("/")
async def root():
    return {"message": "API is running!"}
