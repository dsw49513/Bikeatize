from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime
from sqlalchemy.sql import func

# Tworzenie klasy bazowej dla modeli SQLAlchemy
Base = declarative_base()

# Model użytkownika
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Unikalny identyfikator użytkownika
    name = Column(String(50), nullable=False)  # Imię użytkownika max 50 znaków
    email = Column(String(100), nullable=False, unique=True, index=True)
    hashed_password = Column(String(255), nullable=False)  # Hasło użytkownika (hashowane)
    refresh_token = Column(String(512), nullable=True)  # Refresh token do autoryzacji

    # Relacje z innymi tabelami
    bt_points = relationship("BTPoints", back_populates="user")  # Punkty BT użytkownika
    locations = relationship("Location", back_populates="user")  # Użytkownik może mieć wiele zapisanych lokalizacji
    trips = relationship("Trip", back_populates="user")  # Użytkownik może mieć wiele tras

# Model zapisu lokalizacji
class Location(Base):
    __tablename__ = "locations"  # Nazwa tabeli w bazie

    location_id = Column(Integer, primary_key=True, autoincrement=True, index=True)  # Unikalny identyfikator lokalizacji
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Powiązanie lokalizacji z użytkownikiem
    latitude = Column(Float, nullable=False)  # Szerokość geograficzna lokalizacji
    longitude = Column(Float, nullable=False)  # Długość geograficzna lokalizacji
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)  # Czas zapisu lokalizacji (UTC)

    user = relationship("User", back_populates="locations")  # Relacja lokalizacji z użytkownikiem

# Model zapisu trasy
class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True, autoincrement=True)  # Unikalny identyfikator trasy
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Powiązanie trasy z użytkownikiem
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)  # Czas rozpoczęcia trasy
    end_time = Column(DateTime, nullable=True)  # Czas zakończenia trasy (opcjonalnie)
    total_distance = Column(Float, default=0.0)  # Dystans po zakończeniu trasy

    locations = relationship("TripLocation", back_populates="trip")  # Powiązane lokalizacje trasy
    user = relationship("User", back_populates="trips")  # Powiązanie trasy z użytkownikiem

# Model punktów zapisu trasy
class TripLocation(Base):
    __tablename__ = "trip_locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True)  # Unikalny identyfikator punktu na trasie
    trip_id = Column(Integer, ForeignKey("trips.trip_id"), nullable=False)  # Powiązanie lokalizacji z trasą
    latitude = Column(Float, nullable=False)  # Szerokość geograficzna
    longitude = Column(Float, nullable=False)  # Długość geograficzna
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)  # Czas zapisu punktu trasy

    trip = relationship("Trip", back_populates="locations")  # Powiązanie punktu trasy z trasą

# Model punktów za przejechane trasy BT
class BTPoints(Base):
    __tablename__ = "bt_points"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Unikalny identyfikator punktów BT
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Powiązanie punktów z użytkownikiem
    points = Column(Integer, default=0)  # Liczba zdobytych punktów BT
    achievement_name = Column(String(255))  # Nazwa osiągnięcia
    achieved_at = Column(DateTime, server_default=func.now(), nullable=False)  # Czas zdobycia osiągnięcia

    user = relationship("User", back_populates="bt_points")  # Powiązanie punktów z użytkownikiem
