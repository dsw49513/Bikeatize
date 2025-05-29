from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.database import get_db
from database.models import User
from backend.schemas import UserCreate, Token
from backend.core.security import get_password_hash, verify_password, create_access_token
from backend.schemas.user import UserLogin

router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email już zarejestrowany")

    hashed_pw = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token({"sub": new_user.email, "user_id": new_user.id})
    return {
    "access_token": access_token,
    "refresh_token": "dummy-refresh-token",  # ← tymczasowa wartość
    "token_type": "bearer"
}


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    user_obj = result.scalar_one_or_none()

    if not user_obj or not verify_password(user.password, user_obj.hashed_password):
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane logowania")

    access_token = create_access_token(data={"sub": user_obj.email, "user_id": user_obj.id})
    return {
    "access_token": access_token,
    "refresh_token": "dummy-refresh-token",  # ← tymczasowa wartość
    "token_type": "bearer"
}

