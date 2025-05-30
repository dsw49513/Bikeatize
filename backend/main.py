from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # Middleware CORS dla frontendu

# Import funkcji inicjalizującej bazę danych
from database.database import init_db
from backend.routes.geolocation import router as geolocation_router
from backend.routes.auth import router as auth_router  # Router autoryzacji
from backend.routes.distance import router as distance_router
# Endpointy do mierzenia trasy start stop
from backend.routes.trips import router as trips_router
# potrzebne do pobrania użytkowników przez frontened
from backend.routes.users import router as users_router
from backend.routes.bt_points import router as bt_points_router
from backend.routes.api_router import router as api_router


# Tworzenie aplikacji FastAPI
app = FastAPI()

# Lista dozwolonych originów (adresów frontendów)
origins = [
    "http://localhost:3000",  # Adres Twojego frontendu React
    "http://127.0.0.1:3000",  # Alternatywny adres lokalny
]

# Otwarcie dostępu dla frontendu
app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rejestracja routerów

app.include_router(geolocation_router, prefix="/api")  # Endpointy lokalizacji
# Endpointy związane z autoryzacją
app.include_router(auth_router, prefix="/api")
# Endpointy do zliczania kilometrów
app.include_router(distance_router, prefix="/api")
# Endpointy do mierzenia trasy start-stop
app.include_router(trips_router, prefix="/api")
# Endpoint do pobierania użytkowników
app.include_router(users_router, prefix="/api")
app.include_router(bt_points_router, prefix="/api")
app.include_router(api_router, prefix="/api")


# Endpoint testowy, aby sprawdzić, czy API działa


@app.get("/")
async def root():
    return {"message": "API is running!"}
