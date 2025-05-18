from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    password = Column(String(255), nullable=False)
    refresh_token = Column(String(512), nullable=True)  # Przechowanie refresh token
