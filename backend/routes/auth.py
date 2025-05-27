from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.database import get_db
from models.user import User
from schemas.user import UserCreate, UserLogin, Token
from core.security import get_password_hash, verify_password, create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from database.models import User


router = APIRouter()

@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Rejestracja nowego użytkownika.
    """
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email już zarejestrowany")

    hashed_pw = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token(data={"sub": new_user.email, "user_id": new_user.id})
    return {"access_token": access_token, "token_type": "bearer"}



@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    """
    Logowanie użytkownika.
    """
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Nieprawidłowe dane logowania")

    access_token = create_access_token(data={"sub": user.email, "user_id": user.id})
    return {"access_token": access_token, "token_type": "bearer"}
