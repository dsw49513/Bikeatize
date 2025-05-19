from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
import os

# Ładowanie zmiennych środowiskowych
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("Brak zmiennej DATABASE_URL w .env!")  # Zapobiega uruchomieniu aplikacji bez konfiguracji

# Tworzenie silnika bazy danych
engine = create_async_engine(DATABASE_URL, future=True)

# Sesja asynchroniczna
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Deklaracja bazy danych dla modeli
Base = declarative_base()

# Funkcja inicjalizująca bazę danych (opcjonalnie), wykorzystywany jest alembic do tego
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
