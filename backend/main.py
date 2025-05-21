from fastapi import FastAPI
from database.database import init_db  # Import funkcji inicjalizującej bazę danych
from backend.routes.geolocation import router as geolocation_router
from backend.auth import router as auth_router  # Router autoryzacji
from backend.routes.distance import router as distance_router
from backend.routes.trips import router as trips_router 

# Tworzenie aplikacji FastAPI
app = FastAPI()

# Wywołanie inicjalizacji bazy danych przy starcie serwera
@app.on_event("startup")
async def startup_event():
    await init_db()

# Rejestracja routerów
app.include_router(geolocation_router)  # Endpointy lokalizacji
app.include_router(auth_router)  # Endpointy związane z autoryzacją
app.include_router(distance_router)  # Endpointy do zliczania kilometrów
app.include_router(trips_router)  # Endpointy do mierzenia trasy start stop

# Endpoint testowy
@app.get("/")
async def root():
    return {"message": "API is running!"}


