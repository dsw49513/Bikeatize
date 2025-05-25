from sqlalchemy import Column, Integer, String
from database.database import Base

class User(Base):
    """
    Model użytkownika w bazie danych.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    email = Column(String(100), unique=True, index=True)
    hashed_password = Column(String(128))
