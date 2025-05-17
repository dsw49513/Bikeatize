from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from backend.utils import verify_password  # Import funkcji do sprawdzania hasła
from database.database import SessionLocal
from database.models import User

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/login")
async def login(username: str, password: str, db: AsyncSession = Depends(get_db)):
    user = await db.execute(select(User).where(User.name == username))
    user = user.scalars().first()
    
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")
    
    return {"message": "Login successful"}
