from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from database.database import get_db
from fastapi import HTTPException
# Importujemy funkcję do obliczania dystansu
from backend.utils import calculate_distance
from pydantic import BaseModel

# Router dla endpointow
router = APIRouter()


# Definicja endpointu dla rozpoczecia trasy
@router.post("/start_trip/{user_id}")
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
            # Obsługa błędu jeśli nie uda się pobrać trip_id debugging
            raise ValueError("Nie udało się pobrać trip_id!")

        return {"trip_id": trip_id, "message": "Trasa rozpoczęta."}
    except Exception as e:
        print(f" Błąd w start_trip: {e}")  # Log bledow
        return {"error": str(e)}


class LocationUpdate(BaseModel):
    latitude: float
    longitude: float

# Endpoint do aktualizacji lokalizacji


@router.post("/update_location/{trip_id}")
async def update_location(trip_id: int, location: LocationUpdate, db: AsyncSession = Depends(get_db)):
    #  umieszczana jest lokalizacja do bazy danych
    query = await db.execute(
        text("INSERT INTO trip_locations (trip_id, latitude, longitude, timestamp) VALUES (:trip_id, :lat, :lon, NOW())"),
        {"trip_id": trip_id, "lat": location.latitude, "lon": location.longitude}
    )
    await db.commit()  # Zapisujemy zmiany w bazie danych

    return {"trip_id": trip_id, "message": "Lokalizacja zapisana!"}


def calculate_points(distance: float) -> int:
    points = 0

    if distance <= 10:
        # 10 pkt za każdy km do 10 km
        points = distance*10
    elif distance <= 20:
        # podwójna premia powyżej 10 km
        points = 100 + (distance - 10) * 20
    elif distance <= 30:
        # potrójna premia powyżej 20 km
        points = 300 + (distance - 20) * 30
    elif distance <= 50:
        # poczwórna premia powyżej 30 km
        points = 600 + (distance - 30) * 40
    else:
        # popiątna premia powyżej 50 km
        points = 1400 + (distance - 50) * 50

    return int(points)


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

    # Oblicza punkty na podstawie dystansu
    points_earned = calculate_points(total_distance)
    # Aktualizuje rekord trasy, dodając jej zakończenie oraz całkowity dystans
    await db.execute(
        text("UPDATE trips SET end_time = NOW(), total_distance = :distance WHERE trip_id = :trip_id"),
        {"distance": total_distance, "trip_id": trip_id}
    )
    # Dodaj punkty użytkownikowi
    user_query = await db.execute(
        text("SELECT user_id FROM trips WHERE trip_id = :trip_id"),
        {"trip_id": trip_id}
    )
    user_id = user_query.scalar()
    await db.execute(
        text("UPDATE users SET points = points + :points WHERE id = :user_id"),
        {"points": points_earned, "user_id": user_id}
    )
    await db.commit()  # Zapis zmiany w bazie danych

    return {"trip_id": trip_id, "total_distance_km": total_distance,  "points_earned": points_earned, "message": "Trasa zakończona!"}


# Endpoint do pobrania historii tras użytkownika
@router.get("/trip_history/{user_id}")
async def trip_history(user_id: int, db: AsyncSession = Depends(get_db)):
    # Pobiera wszystkie trasy dla danego użytkownika, sortując od najnowszych
    query = await db.execute(
        text("SELECT trip_id, start_time, end_time, total_distance FROM trips WHERE user_id = :user_id ORDER BY start_time DESC"),
        {"user_id": user_id}
    )
    trips = query.fetchall()

    # Formatuje dane wyjściowe jako listę
    trip_data = [
        {"trip_id": trip[0], "start_time": trip[1],
            "end_time": trip[2], "total_distance_km": trip[3]}
        for trip in trips
    ]

    return {"user_id": user_id, "trips": trip_data}


@router.get("/ranking")
async def get_ranking(session: AsyncSession = Depends(get_db)):
    result = await session.execute(
        text("SELECT name, points FROM users ORDER BY points DESC")
    )
    ranking = result.fetchall()

    return [{"name": row[0], "points": row[1]} for row in ranking]

# Endpoint do usuwania trasy
@router.delete("/delete/{trip_id}")
async def delete_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    try:
        # Usunięcie lokalizacji powiązanych z trasą
        await db.execute(
            text("DELETE FROM trip_locations WHERE trip_id = :trip_id"),
            {"trip_id": trip_id}
        )
        # Usunięcie trasy
        await db.execute(
            text("DELETE FROM trips WHERE trip_id = :trip_id"),
            {"trip_id": trip_id}
        )
        await db.commit()
        return {"message": f"Trasa {trip_id} została usunięta"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=f"Błąd podczas usuwania trasy: {str(e)}")


# Endpoint do sumy dystansu dla użytkownika
@router.get("/total_distance/{user_id}")
async def get_total_distance(user_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(
        text("SELECT SUM(total_distance) FROM trips WHERE user_id = :user_id"),
        {"user_id": user_id}
    )
    result = query.scalar() or 0.0
    return {"user_id": user_id, "total_distance": round(result, 2)}