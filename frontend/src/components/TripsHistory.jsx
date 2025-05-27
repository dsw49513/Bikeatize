import React, { useEffect, useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { jwtDecode } from "jwt-decode";


const TripsHistory = () => {
  const { token } = useContext(AuthContext); // Pobieramy token JWT z kontekstu uwierzytelnienia
  const [trips, setTrips] = useState([]); // Stan do przechowywania listy tras
  const [loading, setLoading] = useState(true); // Flaga ładowania

  useEffect(() => {
    if (!token) return; // Jeżeli nie mamy tokenu, nie wykonujemy zapytania

    // Dekodowanie tokenu JWT w celu uzyskania user_id
    const decoded = jwtDecode(token);
    console.log("Zdekodowany token JWT:", decoded);
    const userId = decoded.user_id; // Zakładamy, że backend zapisuje user_id jako "sub"

    // Pobieranie historii tras z backendu
    fetch(`http://localhost:8000/trip_history/${userId}`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Odpowiedź z backendu:", data);
        setTrips(data?.trips || []); // Zapisanie danych tras w stanie
        setLoading(false); // Wyłączenie trybu ładowania
      })
      .catch((err) => {
        console.error("Błąd pobierania historii tras:", err);
        setLoading(false);
      });
  }, [token]);

  if (loading) return <p>⏳ Ładowanie historii tras...</p>;

  return (
    <section>
      <h3>🛣️ Historia tras:</h3>
      {trips.length === 0 ? (
        <p>Brak zapisanych tras.</p>
      ) : (
        <ul>
          {trips.map((trip) => (
            <li key={trip.trip_id}>
              <strong>Trasa #{trip.trip_id}</strong> | Start: {new Date(trip.start_time).toLocaleString()} | Koniec:{" "}
              {trip.end_time ? new Date(trip.end_time).toLocaleString() : "Trwa"} | Dystans: {trip.total_distance_km} km
            </li>
          ))}
        </ul>
      )}
    </section>
  );
};

export default TripsHistory;
