from fastapi import APIRouter, Depends, HTTPException, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.database import get_db
from database.models import User
from backend.schemas import UserCreate, Token
from backend.core.security import get_password_hash, verify_password, create_access_token
from backend.schemas.user import UserLogin
from backend.core.security import create_refresh_token
import os
from dotenv import load_dotenv
from jwt import PyJWTError as JWTError, decode as jwt_decode, ExpiredSignatureError

router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Brak zmiennej SECRET_KEY w pliku .env!")
ALGORITHM = "HS256"


@router.post("/register", response_model=Token)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email już zarejestrowany")

    hashed_pw = get_password_hash(user.password)
    refresh_token = create_refresh_token({"sub": user.email})
    new_user = User(name=user.name, email=user.email,
                    hashed_password=hashed_pw)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    access_token = create_access_token(
        {"sub": new_user.email, "user_id": new_user.id})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/login", response_model=Token)
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user.email))
    user_obj = result.scalar_one_or_none()

    if not user_obj or not verify_password(user.password, user_obj.hashed_password):
        raise HTTPException(
            status_code=401, detail="Nieprawidłowe dane logowania")

    refresh_token = create_refresh_token({"sub": user_obj.email})
    user_obj.refresh_token = refresh_token
    await db.commit()

    access_token = create_access_token(
        data={"sub": user_obj.email, "user_id": user_obj.id})
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
async def logout(authorization: str = Header(...), db: AsyncSession = Depends(get_db)):
    try:

        if not authorization.startswith("Bearer "):
            raise HTTPException(
                status_code=401, detail="Nieprawidłowy nagłówek Authorization")
        token = authorization.split(" ")[1]

        try:
            payload = jwt_decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            email = payload.get("sub")
        except ExpiredSignatureError:

            return {"message": "Token wygasł, ale wylogowano lokalnie."}
        if not email:
            raise HTTPException(status_code=401, detail="Błędny token")

        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user:
            raise HTTPException(
                status_code=404, detail="Użytkownik nie znaleziony")

        user.refresh_token = None
        await db.commit()

        return {"message": "Wylogowano pomyślnie"}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Błąd podczas wylogowywania: {str(e)}")


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt_decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise HTTPException(status_code=401, detail="Błędny refresh token")

        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        if not user or user.refresh_token != refresh_token:
            raise HTTPException(
                status_code=401, detail="Nieprawidłowy refresh token")

        # Wygeneruj nowy access token
        access_token = create_access_token(
            {"sub": user.email, "user_id": user.id})
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,  # Możesz zwrócić ten sam refresh token
            "token_type": "bearer"
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Błędny refresh token")
