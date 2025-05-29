# Router API (FASTAPI)
from fastapi import APIRouter
from backend.routes.geolocation import router as geolocation_router
from backend.routes.distance import router as distance_router  
from routes import auth
from backend.routes import bt_points

# Tworzenie głównego routera
router = APIRouter()

# Rejestracja poszczególnych routerów
app.include_router(auth.router, prefix="/auth", tags=["auth"]) # Router autoryzacji
app.include_router(bt_points.router, prefix="/api")
router.include_router(geolocation_router)
router.include_router(distance_router)  # API do liczenia kilometrów

# Endpoint który sprawdza status API
@router.get("/status")
def get_status():
       # prosta odpowiedz potwierdzającą działanie API
    return {"message": "API is working!"}
