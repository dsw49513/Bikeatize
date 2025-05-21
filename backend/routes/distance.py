# Implementacja algorytmu Haversine

from fastapi import APIRouter, Depends
from math import radians, sin, cos, sqrt, atan2
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text 
from typing import Dict 

router = APIRouter()

def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Promień Ziemi w km
    lat1, lon1, lat2, lon2 = map(radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    
    return R * c

@router.get("/distance/{user_id}", response_model=Dict[str, float])  # Typ zwracanej wartości
async def calculate_distance(user_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(text("SELECT latitude, longitude FROM locations WHERE user_id = :user_id ORDER BY timestamp ASC"), {"user_id": user_id})
    locations = query.all()  # Używamy .all()

    if not locations or len(locations) < 2:  # Sprawdzanie liczby lokalizacji
        return {"user_id": float(user_id), "total_distance_km": 0.0}  # Typ float

    total_distance = sum(
        haversine(locations[i][0], locations[i][1], locations[i + 1][0], locations[i + 1][1])
        for i in range(len(locations) - 1)
    )

    return {"user_id": float(user_id), "total_distance_km": round(total_distance, 2)}  # Zaokrąglenie do 2 miejsc
