
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from database.database import get_db
from backend.utils import calculate_distance
from pydantic import BaseModel
from datetime import datetime


router = APIRouter()


# Model danych dla aktualizacji lokalizacji
class LocationUpdate(BaseModel):
    latitude: float
    longitude: float


# 🎯 Logika naliczania punktów za dystans
def calculate_points(distance: float) -> int:
    points = 0

    if distance <= 10:
        points = distance * 10
    elif distance <= 20:
        points = 100 + (distance - 10) * 20
    elif distance <= 30:
        points = 300 + (distance - 20) * 30
    elif distance <= 50:
        points = 600 + (distance - 30) * 40
    else:
        points = 1400 + (distance - 50) * 50

    return int(points)


# 🏆 Nowa funkcja: sprawdzanie osiągnięć użytkownika
def check_achievements(distance: float, start_time: datetime) -> list[str]:
    achievements = []

    # Osiągnięcie: jazda nocna (22:00–06:00)
    if start_time.hour >= 22 or start_time.hour < 6:
        achievements.append("🌙 Jazda nocna")

    # Osiągnięcia za pokonany dystans
    if distance >= 10:
        achievements.append("🚴 Przejechano 10 km")
    if distance >= 20:
        achievements.append("🔥 Dystans 20 km – niezły wynik!")
    if distance >= 30:
        achievements.append("🏅 Ponad 30 km – gratulacje!")
    if distance >= 50:
        achievements.append("💪 50 km – masz moc!")

    return achievements


# 🚦 Endpoint: rozpoczęcie trasy
@router.post("/start_trip/{user_id}")
async def start_trip(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            text("SELECT trip_id FROM trips WHERE user_id = :user_id AND end_time IS NULL"),
            {"user_id": user_id}
        )
        active_trip = result.scalar()
        if active_trip:
            return {"trip_id": active_trip}

        await db.execute(
            text("INSERT INTO trips (user_id, start_time) VALUES (:user_id, NOW())"),
            {"user_id": user_id}
        )
        await db.commit()

        trip_id_query = await db.execute(text("SELECT LAST_INSERT_ID()"))
        trip_id = trip_id_query.scalar()

        if trip_id is None:
            raise ValueError("Nie udało się pobrać trip_id!")
        await db.commit()
        return {"trip_id": trip_id, "message": "Trasa rozpoczęta."}
    except Exception as e:
        return {"error": str(e)}


# 📍 Endpoint: aktualizacja lokalizacji
@router.post("/update_location/{trip_id}")
async def update_location(trip_id: int, location: LocationUpdate, db: AsyncSession = Depends(get_db)):
    await db.execute(
        text("INSERT INTO trip_locations (trip_id, latitude, longitude, timestamp) VALUES (:trip_id, :lat, :lon, NOW())"),
        {"trip_id": trip_id, "lat": location.latitude, "lon": location.longitude}
    )
    await db.commit()
    return {"trip_id": trip_id, "message": "Lokalizacja zapisana!"}


# ⛔ Endpoint: zakończenie trasy + naliczanie punktów i osiągnięć
@router.post("/stop_trip/{trip_id}")
async def stop_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    # Pobranie lokalizacji trasy
    query = await db.execute(
        text("SELECT latitude, longitude FROM trip_locations WHERE trip_id = :trip_id ORDER BY timestamp"),
        {"trip_id": trip_id}
    )
    locations = query.fetchall()

    # Oblicz dystans
    total_distance = calculate_distance(locations)

    # Oblicz punkty
    points_earned = calculate_points(total_distance)

    # Pobierz datę rozpoczęcia trasy
    start_time_query = await db.execute(
        text("SELECT start_time FROM trips WHERE trip_id = :trip_id"),
        {"trip_id": trip_id}
    )
    start_time = start_time_query.scalar()

    if start_time is None:
        raise HTTPException(
            status_code=404, detail="Nie znaleziono start_time dla tej trasy.")
    # Sprawdź osiągnięcia
    achievements = check_achievements(total_distance, start_time)

    # Zakończ trasę + zapisz dystans
    await db.execute(
        text("UPDATE trips SET end_time = NOW(), total_distance = :distance WHERE trip_id = :trip_id"),
        {"distance": total_distance, "trip_id": trip_id}
    )

    # Pobierz user_id z trasy

    # Pobiera ID użytkownika powiązanego z trasą

    user_query = await db.execute(
        text("SELECT user_id FROM trips WHERE trip_id = :trip_id"),
        {"trip_id": trip_id}
    )
    user_id = user_query.scalar()

    # Dodaj punkty za dystans + osiągnięcia
    total_points = points_earned + len(achievements) * 50

    await db.execute(
        text("UPDATE users SET points = points + :points WHERE id = :user_id"),
        {"points": total_points, "user_id": user_id}
    )
    await db.commit()

    return {
        "trip_id": trip_id,
        "total_distance_km": round(total_distance, 2),
        "points_earned": total_points,
        "achievements": achievements,
        "message": "Trasa zakończona!"
    }


@router.get("/active_trip/{user_id}")
async def get_active_trip(user_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        text("SELECT trip_id FROM trips WHERE user_id = :user_id AND end_time IS NULL"),
        {"user_id": user_id}
    )
    trip_id = result.scalar()
    return {"trip_id": trip_id}

# 📜 Historia tras użytkownika


@router.get("/trip_history/{user_id}")
async def trip_history(user_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(
        text("SELECT trip_id, start_time, end_time, total_distance FROM trips WHERE user_id = :user_id ORDER BY start_time DESC"),
        {"user_id": user_id}
    )
    trips = query.fetchall()
    trip_data = [
        {
            "trip_id": t[0],
            "start_time": t[1],
            "end_time": t[2],
            "total_distance_km": round(t[3], 2) if t[3] is not None else 0.0
        }
        for t in trips
    ]
    return {"user_id": user_id, "trips": trip_data}


# 🏆 Ranking użytkowników
@router.get("/ranking")
async def get_ranking(filter: str = "global", session: AsyncSession = Depends(get_db)):
    if filter == "weekly":
        result = await session.execute(
            text("""
                SELECT users.name, trips.total_distance
                FROM users
                JOIN trips ON users.id = trips.user_id
                WHERE trips.end_time >= NOW() - INTERVAL 7 DAY
            """)
        )
        trips = result.fetchall()

        user_points = {}
        for trip in trips:
            name = trip[0]
            distance = trip[1]
            points = calculate_points(distance)

            if name in user_points:
                user_points[name] += points
            else:
                user_points[name] = points

        ranking = sorted(user_points.items(), key=lambda x: x[1], reverse=True)
        return [{"name": user[0], "points": user[1]} for user in ranking]

    else:

        result = await session.execute(
            text("SELECT name, points FROM users ORDER BY points DESC")
        )
        ranking = result.fetchall()
        return [{"name": row[0], "points": row[1]} for row in ranking]

# ❌ Usunięcie trasy


@router.delete("/delete/{trip_id}")
async def delete_trip(trip_id: int, db: AsyncSession = Depends(get_db)):
    try:
        await db.execute(
            text("DELETE FROM trip_locations WHERE trip_id = :trip_id"),
            {"trip_id": trip_id}
        )
        await db.execute(
            text("DELETE FROM trips WHERE trip_id = :trip_id"),
            {"trip_id": trip_id}
        )
        await db.commit()
        return {"message": f"Trasa {trip_id} została usunięta"}
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))


# ➕ Suma dystansu
@router.get("/total_distance/{user_id}")
async def get_total_distance(user_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(
        text("SELECT SUM(total_distance) FROM trips WHERE user_id = :user_id"),
        {"user_id": user_id}
    )
    result = query.scalar() or 0.0
    return {"user_id": user_id, "total_distance": round(result, 2)}
