# Skrypt do testu szyfrowania haseł
import sys
sys.path.append("D:\\Bikeatize")  # Dodaj główny katalog do ścieżki Pythona

from backend.utils import hash_password
from database.database import SessionLocal
from sqlalchemy.sql import text
import asyncio

async def main():
    async with SessionLocal() as db:  # Asynchroniczna sesja
        await db.execute(text("DELETE FROM users"))
        await db.commit()

        # Dodanie użytkowników z poprawnie zaszyfrowanymi hasłami
        users = [
            {"name": "Kacper", "password": hash_password("Majg12!")},
            {"name": "Maciej", "password": hash_password("Maciek123")},
            {"name": "Paweł", "password": hash_password("Pawel456")}
        ]

        for user in users:
            await db.execute(text("INSERT INTO users (name, password) VALUES (:name, :password)"), user)

        await db.commit()
        print("Użytkownicy zostali zresetowani ponownie")

# Uruchomienie skryptu
asyncio.run(main())
