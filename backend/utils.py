# Szyfrowanie haseł
import bcrypt
from geopy.distance import geodesic

def hash_password(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def calculate_distance(locations: list[tuple[float, float]]) -> float:
    """
    Oblicza całkowity dystans przebytej trasy na podstawie zapisanych lokalizacji.

    :param locations: Lista zawierających współrzędne GPS (latitude, longitude).
    :return: Całkowity dystans w kilometrach.
    """
    total_distance = 0.0
    
    # Iteruje przez wszystkie punkty na trasie i sumujemy odległość
    for i in range(len(locations) - 1):
        total_distance += geodesic(locations[i], locations[i + 1]).km  # Odległość między dwoma punktami
    
    return round(total_distance, 2)  # Zaokrągla do dwóch miejsc po przecinku
