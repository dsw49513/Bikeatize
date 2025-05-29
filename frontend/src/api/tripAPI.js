const BASE_URL = "http://localhost:8000/api/trips";

// Pobranie historii tras użytkownika
export async function getTripHistory(userId) {
  const res = await fetch(`${BASE_URL}/trip_history/${userId}`);
  if (!res.ok) {
    const err = await res.text();
    throw new Error(`Błąd pobierania historii tras: ${err}`);
  }
  return await res.json();
}

// Usunięcie jednej trasy
export async function deleteTrip(tripId) {
  const res = await fetch(`${BASE_URL}/delete/${tripId}`, {
    method: "DELETE",
  });
  if (!res.ok) {
    throw new Error("Błąd usuwania trasy");
  }
  return await res.json();
}

// Pobranie sumy przejechanych kilometrów
export async function getTotalDistance(userId) {
  const res = await fetch(`${BASE_URL}/total_distance/${userId}`);
  if (!res.ok) {
    throw new Error("Błąd pobierania łącznego dystansu");
  }
  return await res.json();
}
