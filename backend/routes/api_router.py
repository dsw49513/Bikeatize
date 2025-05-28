from fastapi import APIRouter
from backend.routes.geolocation import router as geolocation_router
from backend.routes.auth import router as auth_router
from backend.routes.distance import router as distance_router
from backend.routes.trips import router as trips_router
from backend.routes.users import router as users_router
from backend.routes.bt_points import router as bt_points_router

# Główny agregujący router
router = APIRouter()

# Rejestracja poszczególnych routerów
router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(geolocation_router, prefix="/geolocation", tags=["geolocation"])
router.include_router(distance_router, prefix="/distance", tags=["distance"])
router.include_router(trips_router, prefix="/trips", tags=["trips"])
router.include_router(users_router, prefix="/users", tags=["users"])
router.include_router(bt_points_router, prefix="/points", tags=["bt_points"])
