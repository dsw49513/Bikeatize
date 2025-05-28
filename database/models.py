from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship, declarative_base
from datetime import datetime, timezone

# Klasa bazowa SQLAlchemy
Base = declarative_base()

# Model użytkownika
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)  # Unikalny ID
    name = Column(String(100))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(128))
    refresh_token = Column(String(512), nullable=True)  # opcjonalny refresh token
    points = Column(Integer, default=0)
    total_distance = Column(Float, default=0.0)

    # Relacja 1:N z lokalizacjami i trasami
    locations = relationship("Location", back_populates="user")
    trips = relationship("Trip", back_populates="user")

# Model lokalizacji GPS
class Location(Base):
    __tablename__ = "locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Powiązanie z użytkownikiem
    user = relationship("User", back_populates="locations")

# Model trasy
class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    end_time = Column(DateTime, nullable=True)
    total_distance = Column(Float, default=0.0)

    # Relacja z użytkownikiem i lokalizacjami trasy
    user = relationship("User", back_populates="trips")
    locations = relationship("TripLocation", back_populates="trip")

# Model punktów GPS przypisanych do trasy
class TripLocation(Base):
    __tablename__ = "trip_locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Powiązanie z trasą
    trip = relationship("Trip", back_populates="locations")
