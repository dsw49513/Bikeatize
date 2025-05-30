from datetime import datetime, timedelta
from typing import Optional
import jwt
from jwt import PyJWTError as JWTError
from passlib.context import CryptContext
from fastapi import Depends
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from database.models import User
from database.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import os
from dotenv import load_dotenv

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Brak zmiennej SECRET_KEY w pliku .env!")


# 🔐 Konfiguracja OAuth2
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

# Konfiguracja haszowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Weryfikuje, czy podane hasło odpowiada zahaszowanemu hasłu.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Zwraca zahaszowane hasło.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict):
    """
    Tworzy token JWT z danymi użytkownika.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})  # dodajemy wygaśnięcie
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> User:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=401, detail="Brak user_id w tokenie")
    except JWTError:
        raise HTTPException(status_code=401, detail="Błędny token")

    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="Użytkownik nie istnieje")

    return user


def create_refresh_token(data: dict):
    """
    Tworzy refresh token JWT z danymi użytkownika.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
