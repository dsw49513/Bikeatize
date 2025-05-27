from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext

# Konfiguracja haszowania haseł
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Sekret i algorytm do podpisywania tokenów JWT
SECRET_KEY = "supersekretnyklucz123"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Weryfikuje, czy podane hasło odpowiada zahaszowanemu hasłu.
    """
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """
    Zwraca zahaszowane hasło.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict):
    """
    Tworzy token JWT z danymi użytkownika.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
