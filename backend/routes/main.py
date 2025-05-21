# Router API (FASTAPI)
from fastapi import APIRouter
from backend.routes.geolocation import router as geolocation_router
from backend.routes.distance import router as distance_router  

# Tworzenie głównego routera
router = APIRouter()

# Rejestracja poszczególnych routerów
router.include_router(geolocation_router)
router.include_router(distance_router)  # API do liczenia kilometrów

# Endpoint który sprawdza status API
@router.get("/status")
def get_status():
       # prosta odpowiedz potwierdzającą działanie API
    return {"message": "API is working!"}
