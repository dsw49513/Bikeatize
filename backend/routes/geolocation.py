from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database.database import SessionLocal
from database.models import Location
from backend.schemas import LocationCreate

router = APIRouter()

# Asynchroniczne pobieranie sesji bazy danych
async def get_db():
    async with SessionLocal() as db:
        yield db

# Endpoint do zapisywania lokalizacji użytkownika
@router.post("/location/update")
async def update_location(location: LocationCreate, db: AsyncSession = Depends(get_db)):
    # Tworzenie nowego wpisu lokalizacji
    new_location = Location(
        user_id=location.user_id,
        latitude=location.latitude,
        longitude=location.longitude
    )
    db.add(new_location) # Dodanie nowej lokalizacji do sesji
    await db.commit() # Zapisanie zmian w bazie danych
    await db.refresh(new_location) # Odświeżenie obiektu, aby zawierał zaktualizowane dane
    return {"message": "Lokalizacja zapisana!", "location": new_location}

# Endpoint do pobierania ostatniej zapisanej lokalizacji użytkownika
@router.get("/location/{user_id}")
async def get_location(user_id: int, db: AsyncSession = Depends(get_db)):
    # Pobranie ostatniej zapisanej lokalizacji użytkownika, sortowanie malejąco po location_id
    result = await db.execute(
        select(Location).where(Location.user_id == user_id).order_by(Location.location_id.desc())  # Zmienione na location_id
    )
    location = result.scalars().first() # Pobranie pierwszego wyniku

    if not location:
        raise HTTPException(status_code=404, detail="Lokalizacja nie znaleziona")

    return location # Zwrot obiektu lokalizacji
