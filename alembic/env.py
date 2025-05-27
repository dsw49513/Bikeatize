from dotenv import load_dotenv
import os
import sys
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy.sql import func

# Dodaj katalog główny projektu do sys.path
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), "..", "..")))

# Ładowanie zmiennych środowiskowych z pliku .env
load_dotenv()

# Pobierz URL bazy danych z pliku .env
DATABASE_URL = os.getenv("ALEMBIC_URL")
if not DATABASE_URL:
    raise RuntimeError("Brak zmiennej ALEMBIC_URL w pliku .env!")


config = context.config
fileConfig(config.config_file_name)


Base = declarative_base()


target_metadata = Base.metadata

# Model użytkownika


class User(Base):
    __tablename__ = "users"

    # Unikalny identyfikator użytkownika
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)  # Imię użytkownika max 50 znaków
    email = Column(String(255), unique=True, nullable=False)
    # Hasło użytkownika (hashowane)
    password = Column(String(255), nullable=False)
    # Refresh token do autoryzacji
    refresh_token = Column(String(512), nullable=True)

    # Relacje z innymi tabelami
    # Punkty BT użytkownika
    bt_points = relationship("BTPoints", back_populates="user")
    # Użytkownik może mieć wiele zapisanych lokalizacji
    locations = relationship("Location", back_populates="user")
    # Użytkownik może mieć wiele tras
    trips = relationship("Trip", back_populates="user")

# Model zapisu lokalizacji


class Location(Base):
    __tablename__ = "locations"  # Nazwa tabeli w bazie

    # Unikalny identyfikator lokalizacji
    location_id = Column(Integer, primary_key=True,
                         autoincrement=True, index=True)
    # Powiązanie lokalizacji z użytkownikiem
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    # Szerokość geograficzna lokalizacji
    latitude = Column(Float, nullable=False)
    # Długość geograficzna lokalizacji
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow,
                       nullable=False)  # Czas zapisu lokalizacji (UTC)

    # Relacja lokalizacji z użytkownikiem
    user = relationship("User", back_populates="locations")

# Model zapisu trasy


class Trip(Base):
    __tablename__ = "trips"

    # Unikalny identyfikator trasy
    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    # Powiązanie trasy z użytkownikiem
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow,
                        nullable=False)  # Czas rozpoczęcia trasy
    # Czas zakończenia trasy (opcjonalnie)
    end_time = Column(DateTime, nullable=True)
    total_distance = Column(Float, default=0.0)  # Dystans po zakończeniu trasy

    # Powiązane lokalizacje trasy
    locations = relationship("TripLocation", back_populates="trip")
    # Powiązanie trasy z użytkownikiem
    user = relationship("User", back_populates="trips")

# Model punktów zapisu trasy


class TripLocation(Base):
    __tablename__ = "trip_locations"

    # Unikalny identyfikator punktu na trasie
    location_id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"),
                     nullable=False)  # Powiązanie lokalizacji z trasą
    latitude = Column(Float, nullable=False)  # Szerokość geograficzna
    longitude = Column(Float, nullable=False)  # Długość geograficzna
    timestamp = Column(DateTime, default=datetime.utcnow,
                       nullable=False)  # Czas zapisu punktu trasy

    # Powiązanie punktu trasy z trasą
    trip = relationship("Trip", back_populates="locations")

# Model punktów za przejechane trasy BT


class BTPoints(Base):
    __tablename__ = "bt_points"

    # Unikalny identyfikator punktów BT
    id = Column(Integer, primary_key=True, autoincrement=True)
    # Powiązanie punktów z użytkownikiem
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    points = Column(Integer, default=0)  # Liczba zdobytych punktów BT
    achievement_name = Column(String(255))  # Nazwa osiągnięcia
    achieved_at = Column(DateTime, server_default=func.now(),
                         nullable=False)  # Czas zdobycia osiągnięcia

    # Powiązanie punktów z użytkownikiem
    user = relationship("User", back_populates="bt_points")


def run_migrations_offline():
    context.configure(
        url=DATABASE_URL,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


# Funkcja do migracji online
def run_migrations_online():
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        url=DATABASE_URL,
    )
    with connectable.connect() as connection:
        context.configure(connection=connection,
                          target_metadata=target_metadata)
        with context.begin_transaction():
            context.run_migrations()


# Wybierz tryb migracji (offline/online)
if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
