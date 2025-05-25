from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("Brak zmiennej DATABASE_URL w .env!")

# Tworzenie silnika bazy danych
engine = create_async_engine(DATABASE_URL, future=True)

# Tworzenie sesji bazodanowej
SessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

# Deklaratywna baza do tworzenia modeli
Base = declarative_base()

# Funkcja inicjalizująca bazę danych (dla Alembic lub innych migracji)
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

# ✅ Główna funkcja do pobierania sesji bazy danych – aliasowana jako get_db
async def get_db():
    async with SessionLocal() as session:
        yield session
