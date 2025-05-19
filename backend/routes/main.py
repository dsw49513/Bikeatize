# Router API (FASTAPI)
from fastapi import APIRouter

# Tworzenie głównego routera
router = APIRouter()

# Importowanie i dodanie routera odpowiedzialnego za geolokalizację
from backend.routes.geolocation import router as geolocation_router
router.include_router(geolocation_router)

# Endpoint który sprawdza status API
@router.get("/status")
def get_status():
    # prosta odpowiedz potwierdzającą działanie API
    return {"message": "API is working!"}
