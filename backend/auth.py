from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt
import datetime
from dotenv import load_dotenv
import os
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from .utils import verify_password # Sprawdzanie hasła
from database.database import SessionLocal
from database.models import User

# Wczytanie zmiennych środowiskowych
load_dotenv(dotenv_path="D:/Bikeatize/.env") # Jeśli `.env` - Podaj sciezke do env

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Brak zmiennej SECRET_KEY w .env!")  # Zapobiega uruchomieniu aplikacji bez klucza

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# Model danych dla `/refresh`
class RefreshTokenRequest(BaseModel):
    refresh_token: str

# Model danych dla `/login`
class LoginRequest(BaseModel):
    username: str
    password: str

# Obsługa sesji bazy danych
async def get_db():
    async with SessionLocal() as session:
        yield session

# Funkcja generująca token JWT
def create_jwt(username: str, refresh: bool = False):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + (datetime.timedelta(days=30) if refresh else datetime.timedelta(minutes=15))
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# Middleware do sprawdzania autoryzacji
async def get_current_user(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload.get("sub")

        if not username:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Pobranie użytkownika z bazy
        user = await db.execute(select(User).where(User.name == username))
        user = user.scalars().first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return user  # Zwrot pełnego obiektu użytkownika zamiast samego `name`
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")


# Endpoint logowania użytkownika
@router.post("/login")
async def login(request: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.name == request.username))
    user = user.scalars().first()

    if not user or not verify_password(request.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_jwt(user.name)
    refresh_token = create_jwt(user.name, refresh=True)

    # Zapis refresh tokena w bazie
    user.refresh_token = refresh_token
    await db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}

# Endpoint wylogowania użytkownika
@router.post("/logout")
async def logout(user: User = Depends(get_current_user), db: AsyncSession = Depends(get_db)):
    user.refresh_token = None  # Unieważniamy refresh token
    await db.commit()
    return {"message": "Logged out successfully"}

# Endpoint odświeżania tokena
@router.post("/refresh")
async def refresh_token(request: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    refresh_token = request.refresh_token

    # Sprawdzenie czy refresh token istnieje w bazie
    user = await db.execute(select(User).where(User.refresh_token == refresh_token))
    user = user.scalars().first()

    if not user:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Weryfikacja refresh tokena
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    # Generowanie nowego access token i refresh token
    new_access_token = create_jwt(user.name)
    new_refresh_token = create_jwt(user.name, refresh=True)

    # Aktualizacja refresh token w bazie, unieważniając poprzedni
    user.refresh_token = new_refresh_token
    await db.commit()

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }