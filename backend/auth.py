from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt
import datetime
from backend.utils import verify_password  # Sprawdzanie hasła
from database.database import SessionLocal
from database.models import User

SECRET_KEY = "super_secret_key"  # Przechowana wewnatrz zmiennej srodowiskowej

router = APIRouter()

# Funkcja generująca token JWT
def create_jwt(username: str, refresh: bool = False):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + (datetime.timedelta(days=30) if refresh else datetime.timedelta(minutes=15))
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")


# Funkcja do obsługi sesji bazy danych
async def get_db():
    async with SessionLocal() as session:
        yield session

# Endpoint logowania użytkownika
@router.post("/login")
async def login(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.name == username))
    user = user.scalars().first()
    
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    token = create_jwt(user.name)
    return {"access_token": token, "token_type": "bearer"}

# Odbieranie refresh token i generowanie drugiego access token
@router.post("/refresh")
async def refresh_token(refresh_token: str, db: AsyncSession = Depends(get_db)):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        user = await db.execute(select(User).where(User.name == payload["sub"]))
        user = user.scalars().first()

        if not user:
            raise HTTPException(status_code=401, detail="Invalid refresh token")

        new_access_token = create_jwt(user.name)
        return {"access_token": new_access_token, "token_type": "bearer"}
    
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Refresh token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

