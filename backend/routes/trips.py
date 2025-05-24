from fastapi import APIRouter, Depends  
from sqlalchemy.ext.asyncio import AsyncSession  
from sqlalchemy.sql import text  
from database.database import get_db  
from backend.utils import calculate_distance  # Importujemy funkcję do obliczania dystansu

# Router dla endpointow
router = APIRouter()

@router.post("/start_trip/{user_id}")  # Definicja endpointu dla rozpoczecia trasy
async def start_trip(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        print(f" Start nowej trasy dla user_id: {user_id}")

        # Nowy rekord wstawiany w tabele rozpoczynajacy trase
        await db.execute(
            text("INSERT INTO trips (user_id, start_time) VALUES (:user_id, NOW())"),
            {"user_id": user_id}
        )
        await db.commit()  # Zapis zmiany w tabeli

        # Pobiera ID nowo utworzonej trasy
        trip_id_query = await db.execute(text("SELECT LAST_INSERT_ID()"))
        trip_id = trip_id_query.scalar()

        if trip_id is None:
            raise ValueError("Nie udało się pobrać trip_id!")  # Obsługa błędu jeśli nie uda się pobrać trip_id debugging

        return {"trip_id": trip_id, "message": "Trasa rozpoczęta."}
    except Exception as e:
        print(f" Błąd w start_trip: {e}")  # Log bledow
        return {"error": str(e)}

@router.post("/update_location/{trip_id}")  # Endpoint do aktualizacji lokalizacji
async def update_location(trip_id: int, latitude: float, longitude: float, db: AsyncSession = Depends(get_db)):
    #  umieszczana jest lokalizacja do bazy danych
    query = await db.execute(
        text("INSERT INTO trip_locations (trip_id, latitude, longitude, timestamp) VALUES (:trip_id, :lat, :lon, NOW())"),
        {"trip_id": trip_id, "lat": latitude, "lon": longitude}
    )
    await db.commit()  # Zapisujemy zmiany w bazie danych

    return {"trip_id": trip_id, "message": "Lokalizacja zapisana!"}

@router.post("/stop_trip/{trip_id}")  # Endpoint do zakończenia trasy
async def stop_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    # Pobiera wszystkie lokalizacje dla danej trasy
    query = await db.execute(
        text("SELECT latitude, longitude FROM trip_locations WHERE trip_id = :trip_id ORDER BY timestamp"),
        {"trip_id": trip_id}
    )
    locations = query.fetchall()

    # Oblicza całkowity dystans na podstawie zapisanych lokalizacji
    total_distance = calculate_distance(locations)

    # Aktualizuje rekord trasy, dodając jej zakończenie oraz całkowity dystans
    await db.execute(
        text("UPDATE trips SET end_time = NOW(), total_distance = :distance WHERE trip_id = :trip_id"),
        {"distance": total_distance, "trip_id": trip_id}
    )
    await db.commit()  # Zapis zmiany w bazie danych

    return {"trip_id": trip_id, "total_distance_km": total_distance, "message": "Trasa zakończona!"}

@router.get("/trip_history/{user_id}")  # Endpoint do pobrania historii tras użytkownika
async def trip_history(user_id: int, db: AsyncSession = Depends(get_db)):
    # Pobiera wszystkie trasy dla danego użytkownika, sortując od najnowszych
    query = await db.execute(
        text("SELECT trip_id, start_time, end_time, total_distance FROM trips WHERE user_id = :user_id ORDER BY start_time DESC"),
        {"user_id": user_id}
    )
    trips = query.fetchall()

    # Formatuje dane wyjściowe jako listę
    trip_data = [
        {"trip_id": trip[0], "start_time": trip[1], "end_time": trip[2], "total_distance_km": trip[3]}
        for trip in trips
    ]

    return {"user_id": user_id, "trips": trip_data}


