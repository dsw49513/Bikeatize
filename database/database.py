from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os

# Ładowanie zmiennych środowiskowych
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("Brak zmiennej DATABASE_URL w .env!")  # Zapobiega uruchomieniu aplikacji bez konfiguracji

engine = create_async_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
