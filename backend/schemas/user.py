from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    """
    Schemat danych do rejestracji użytkownika.
    """
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    """
    Schemat danych do logowania użytkownika.
    """
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    """
    Schemat danych zwracanych po operacjach na użytkowniku.
    """
    id: int
    name: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    """
    Schemat tokenu JWT.
    """
    access_token: str
    token_type: str
