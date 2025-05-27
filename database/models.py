from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


# Tworzenie klasy bazowej dla modeli SQLAlchemy
Base = declarative_base()

# Model użytkownika


class User(Base):
    __tablename__ = "users"

    # Unikalny identyfikator użytkownika
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)  # Imię użytkownika max 50 znaków
    email = Column(String(100), nullable=False, unique=True, index=True)
    # Hasło użytkownika (hashowane)
    hashed_password = Column(String(255), nullable=False)
    # refresh token do autoryzacji
    refresh_token = Column(String(512), nullable=True)
    # Punkty użytkownika, domyślnie 0
    points = Column(Integer, nullable=False, default=0)
    # użytkownik moze miec  wiele lokalizacji
    locations = relationship("Location", back_populates="user")

# Model zapisu lokalizacji


class Location(Base):
    __tablename__ = "locations"  # Nazwa tabeli w bazie

    # Unikalny identyfikator lokalizacji
    location_id = Column(Integer, primary_key=True,
                         autoincrement=True, index=True)
    # Powiązanie lokalizacji z użytkownikiem
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    latitude = Column(Float, nullable=False)  # Szerokość geograficzna lokal.
    longitude = Column(Float, nullable=False)  # Długość geograficzna lokal.
    # Czas zapisu lokalizacji (domyślnie czas UTC)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    user = relationship("User", back_populates="locations")

# Model zapisu trasy


class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    total_distance = Column(Float, default=0.0)  # Dystans po zakończeniu trasy

    # Powiązane lokalizacje
    locations = relationship("TripLocation", back_populates="trip")

# Model punktów zapisu trasy


class TripLocation(Base):
    __tablename__ = "trip_locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Powiązanie z trasą
    trip = relationship("Trip", back_populates="locations")
