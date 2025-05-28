import React, { useState, useEffect, useContext, useRef } from "react";
import { AuthContext } from "../context/AuthContext";
import { jwtDecode } from "jwt-decode";

const RideTracker = () => {
  const { token } = useContext(AuthContext); // Token JWT użytkownika
  const [tripId, setTripId] = useState(null); // ID aktualnej trasy
  const [distance, setDistance] = useState(null); // Pokonany dystans
  const intervalRef = useRef(null); // Interwał do wysyłania lokalizacji

  // Funkcja dekodująca token i zwracająca user_id
  const getUserId = () => {
    try {
      const decoded = jwtDecode(token);
      return decoded.user_id;
    } catch (error) {
      console.error("Błąd dekodowania tokena JWT:", error);
      return null;
    }
  };

  // Rozpoczęcie trasy — wywołuje backend i ustawia interwał wysyłania lokalizacji
  const startTrip = async () => {
    const userId = getUserId();
    if (!userId) return;

    try {
      const res = await fetch(`http://localhost:8000/api/start_trip/${userId}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!res.ok) {
        const err = await res.text();
        throw new Error(`Błąd: ${res.status} ${err}`);
      }

      const data = await res.json();
      setTripId(data.trip_id);

      intervalRef.current = setInterval(sendLocationUpdate, 5000); // Co 5 sek. wysyłamy lokalizację
    } catch (err) {
      console.error("Błąd przy rozpoczynaniu trasy:", err);
      alert("Nie udało się rozpocząć trasy.");
    }
  };

  // Wysyłanie bieżącej lokalizacji użytkownika do backendu
  const sendLocationUpdate = () => {
    if (!tripId) return;

    if (!navigator.geolocation) {
      console.error("Geolokalizacja nie jest dostępna w Twojej przeglądarce.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude } = pos.coords;

        try {
          await fetch(
            `http://localhost:8000/api/update_location/${tripId}?latitude=${latitude}&longitude=${longitude}`,
            {
              method: "POST",
              headers: {
                Authorization: `Bearer ${token}`,
                "Content-Type": "application/json",
              },
            }
          );
        } catch (err) {
          console.error("Błąd przy wysyłaniu lokalizacji:", err);
        }
      },
      (err) => {
        console.error("Błąd geolokalizacji:", err);
      }
    );
  };

  // Zakończenie trasy — wysyła żądanie zakończenia i czyści interwał
  const stopTrip = async () => {
    if (!tripId) return;

    clearInterval(intervalRef.current); // Przerwanie interwału

    try {
      const res = await fetch(`http://localhost:8000/api/stop_trip/${tripId}`, {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
          "Content-Type": "application/json",
        },
      });

      if (!res.ok) {
        const err = await res.text();
        throw new Error(`Błąd: ${res.status} ${err}`);
      }

      const data = await res.json();
      setDistance(data.total_distance_km);
      setTripId(null); // Trasa zakończona
    } catch (err) {
      console.error("Błąd przy zatrzymywaniu trasy:", err);
      alert("Nie udało się zakończyć trasy.");
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
