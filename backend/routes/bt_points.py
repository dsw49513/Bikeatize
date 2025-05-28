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
