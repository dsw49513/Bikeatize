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
def create_jwt(username: str):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
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
