import React, { useState, useEffect, useContext, useRef } from "react";
import { AuthContext } from "../context/AuthContext";
import { jwtDecode } from "jwt-decode";

const RideTracker = () => {
  const { token } = useContext(AuthContext); // Pobieramy token JWT
  const [tripId, setTripId] = useState(null); // Przechowuje ID aktualnej trasy
  const [distance, setDistance] = useState(null); // Przechowuje dystans po zakończeniu
  const intervalRef = useRef(null); // Referencja do interwału lokalizacji

  // Funkcja do pobierania user_id z tokena JWT
  const getUserId = () => {
    const decoded = jwtDecode(token);
    return decoded.user_id;
  };

  // Rozpoczęcie trasy
  const startTrip = async () => {
    const userId = getUserId();

    try {
      const res = await fetch(`http://localhost:8000/start_trip/${userId}`, {
        method: "POST",
      });
      const data = await res.json();
      setTripId(data.trip_id);

      // Ustawienie interwału aktualizacji lokalizacji co 5 sekund
      intervalRef.current = setInterval(sendLocationUpdate, 5000);
    } catch (err) {
      console.error("Błąd przy rozpoczynaniu trasy:", err);
    }
  };

  // Wysyłanie aktualnej lokalizacji do backendu
  const sendLocationUpdate = () => {
    if (!tripId) return;

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude } = pos.coords;

        await fetch(`http://localhost:8000/update_location/${tripId}?latitude=${latitude}&longitude=${longitude}`, {
          method: "POST",
        });
      },
      (err) => {
        console.error("Błąd geolokalizacji:", err);
      }
    );
  };

  // Zakończenie trasy
  const stopTrip = async () => {
    if (!tripId) return;

    clearInterval(intervalRef.current); // zatrzymanie interwału

    try {
      const res = await fetch(`http://localhost:8000/stop_trip/${tripId}`, {
        method: "POST",
      });
      const data = await res.json();
      setDistance(data.total_distance_km); // zapisujemy dystans
      setTripId(null); // zerujemy ID trasy
    } catch (err) {
      console.error("Błąd przy zatrzymywaniu trasy:", err);
    }
  };

  return (
    <section>
      <h3>🛰️ Śledzenie trasy:</h3>

      {tripId ? (
        <div>
          <p>Trasa aktywna – ID: {tripId}</p>
          <button onClick={stopTrip}>⏹ Zakończ trasę</button>
        </div>
      ) : (
        <button onClick={startTrip}>▶️ Rozpocznij trasę</button>
      )}

      {distance !== null && (
        <p>📏 Pokonany dystans: {distance} km</p>
      )}
    </section>
  );
};

export default RideTracker;
