# Importowanie klasy bazowej Pydantic do walidacji danych
from pydantic import BaseModel

# Definicja schematu danych do utworzenia lokalizacji użytkownika
class LocationCreate(BaseModel):
    user_id: int  # ID użytkownika, który przesyla lokalizacje
    latitude: float # Szerokosc geograficzna lokalizacji
    longitude: float # Dlugosc geograficzna lokalizacji

class UserCreate(BaseModel):
    username: str
    password: str
    email: str

