from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
import jwt
import datetime
from dotenv import load_dotenv
import os
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

from database.database import SessionLocal
from database.models import User
from backend.schemas.user import UserCreate, Token

# ====== ENV ======
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
load_dotenv(ENV_PATH)

SECRET_KEY = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("Brak zmiennej SECRET_KEY w .env!")

# ====== JWT + PASSWORDS ======
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def create_jwt(username: str, refresh: bool = False):
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + (datetime.timedelta(days=30) if refresh else datetime.timedelta(minutes=15))
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

# ====== DB SESSION ======
async def get_db():
    async with SessionLocal() as session:
        yield session

async def get_user_by_username(username: str, db: AsyncSession):
    result = await db.execute(select(User).where(User.name == username))
    return result.scalars().first()

# ====== ROUTER SETUP ======
router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ====== AUTH ENDPOINTS ======

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await get_user_by_username(user.name, db)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    
    hashed_password = hash_password(user.password)
    new_user = User(name=user.name, hashed_password=hashed_password, email=user.email)
    db.add(new_user)
    await db.commit()
    return {"message": "User created"}

@router.post("/login", response_model=Token)
async def login(request: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.name == request.name))
    user = user.scalars().first()

    if not user or not pwd_context.verify(request.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token = create_jwt(user.name)
    refresh_token = create_jwt(user.name, refresh=True)

    user.refresh_token = refresh_token
    await db.commit()

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
