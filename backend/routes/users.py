from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.database import get_db as get_session
from database.models import User
from pydantic import BaseModel

router = APIRouter()

# Schematy danych


class UserCreate(BaseModel):
    name: str
    email: str


class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True

# CREATE - dodanie użytkownika


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, session: AsyncSession = Depends(get_session)):
    db_user = User(name=user.name, email=user.email)
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

# READ - pobranie wszystkich użytkowników


@router.get("/users", response_model=list[UserResponse])
async def get_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return users

# UPDATE - aktualizacja użytkownika


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, updated_user: UserCreate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=404, detail="Użytkownik nie znaleziony")
    user.name = updated_user.name
    user.email = updated_user.email
    await session.commit()
    return user

# DELETE - usunięcie użytkownika


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(
            status_code=404, detail="Użytkownik nie znaleziony")
    await session.delete(user)
    await session.commit()
    return {"message": "Użytkownik usunięty"}
