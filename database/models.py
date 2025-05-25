from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime


# Tworzenie klasy bazowej dla modeli SQLAlchemy
Base = declarative_base()

# Model użytkownika
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True) # Unikalny identyfikator użytkownika
    name = Column(String(50), nullable=False)# Imię użytkownika max 50 znaków
    password = Column(String(255), nullable=False) # Hasło użytkownika (hashowane)
    refresh_token = Column(String(512), nullable=True)  # refresh token do autoryzacji

    locations = relationship("Location", back_populates="user") # użytkownik moze miec  wiele lokalizacji

# Model zapisu lokalizacji
class Location(Base):
    __tablename__ = "locations" # Nazwa tabeli w bazie

    location_id = Column(Integer, primary_key=True, autoincrement=True, index=True) # Unikalny identyfikator lokalizacji
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Powiązanie lokalizacji z użytkownikiem
    latitude = Column(Float, nullable=False) # Szerokość geograficzna lokal.
    longitude = Column(Float, nullable=False) # Długość geograficzna lokal.
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False) # Czas zapisu lokalizacji (domyślnie czas UTC)

    user = relationship("User", back_populates="locations")

# Model zapisu trasy
class Trip(Base):
    __tablename__ = "trips"

    trip_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    start_time = Column(DateTime, default=datetime.utcnow, nullable=False)
    end_time = Column(DateTime, nullable=True)
    total_distance = Column(Float, default=0.0)  # Dystans po zakończeniu trasy

    locations = relationship("TripLocation", back_populates="trip")  # Powiązane lokalizacje

# Model punktów zapisu trasy
class TripLocation(Base):
    __tablename__ = "trip_locations"

    location_id = Column(Integer, primary_key=True, autoincrement=True)
    trip_id = Column(Integer, ForeignKey("trips.trip_id"), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow, nullable=False)

    trip = relationship("Trip", back_populates="locations")  # Powiązanie z trasą