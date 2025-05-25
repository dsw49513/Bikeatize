from pydantic import BaseModel

class LocationCreate(BaseModel):
    user_id: int
    latitude: float
    longitude: float
