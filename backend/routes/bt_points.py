
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from backend.core.security import get_current_user
from database.database import get_db
from database.models import User

router = APIRouter()

@router.get("/bt_points/me")
async def get_my_points(
    session: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {
        "points": current_user.points,
        "total_distance": current_user.total_distance
    }
=======
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import text
from database.database import get_db

# Inicjalizacja routera
router = APIRouter()

RANKS = [
    (0, "Beginner Rider"),
    (100, "Intermediate Rider "),
    (500, "Expert Rider"),
    (1000, "Master Rider"),
    (5000, "Legend of Bikeatize")
]

# Funkcja przyznająca punkty i zwracająca aktualną rangę
@router.post("/award_bt_points/{user_id}")
async def award_bt_points(user_id: int, distance: float, db: AsyncSession = Depends(get_db)):
    points = int(distance * 10)  # 10 pkt za każdy km

    if distance < 1.0:
        print(f"Dystans zbyt mały ({distance} km), nie przyznano BT Points")
        return {"message": "Dystans zbyt mały, nie przyznano punktów"}

    try:
        await db.execute(
            text("INSERT INTO bt_points (user_id, points, achievement_name, achieved_at) VALUES (:user_id, :points, :name, NOW())"),
            {"user_id": user_id, "points": points, "name": "Trasa zakończona!"}
        )
        await db.commit()

        # Pobranie sumy punktów użytkownika
        result = await db.execute(
            text("SELECT COALESCE(SUM(points), 0) AS total_points FROM bt_points WHERE user_id = :user_id"),
            {"user_id": user_id}
        )
        total_points = result.scalar() or 0

        # Wybór odpowiedniej rangi
        user_rank = "Beginner Raider"
        for rank_points, rank_name in RANKS:
            if total_points >= rank_points:
                user_rank = rank_name

        return {
            "user_id": user_id,
            "awarded_points": points,
            "total_points": total_points,
            "rank": user_rank,
            "message": f"Zdobyto {points} punktów! Aktualna ranga: {user_rank}"
        }
    except Exception as e:
        await db.rollback()
        print(f"Błąd zapisu BT Points: {e}")
        return {"message": "Wystąpił błąd, spróbuj ponownie"}

# Endpoint do pobierania punktów użytkownika
@router.get("/user_points/{user_id}")
async def get_user_points(user_id: int, db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(
            text("SELECT COALESCE(SUM(points), 0) AS total_points FROM bt_points WHERE user_id = :user_id"),
            {"user_id": user_id}
        )

        total_points = result.scalar() or 0
        return {"user_id": user_id, "total_points": total_points}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd pobierania punktów: {e}")

