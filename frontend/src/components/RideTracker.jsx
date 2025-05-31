import React, { useState, useContext, useRef, useEffect } from "react";
import { AuthContext } from "../context/AuthContext";
import { jwtDecode } from "jwt-decode";

const RideTracker = ({ onTripStarted, onTripStopped }) => {
  const { token } = useContext(AuthContext);
  const [tripId, setTripId] = useState(null);
  const [distance, setDistance] = useState(null);
  const [points, setPoints] = useState(null);
  const [achievements, setAchievements] = useState([]);
  const intervalRef = useRef(null);
  
  useEffect(() => {
 
  if (tripId) {
    intervalRef.current = setInterval(sendLocationUpdate, 5000);
  } else {
    clearInterval(intervalRef.current);
  }
  
  return () => clearInterval(intervalRef.current);
}, [tripId]);
useEffect(() => {
    const fetchActiveTrip = async () => {
      if (!token) return;
      try {
        const userId = getUserId();
        const res = await fetch(`http://localhost:8000/api/active_trip/${userId}`, {
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
        });
        if (res.ok) {
          const data = await res.json();
          if (data.trip_id) setTripId(data.trip_id);
        }
      } catch (err) {
        console.error("Błąd pobierania aktywnej trasy:", err);
      }
    };
    fetchActiveTrip();
  }, [token]);
  const getUserId = () => {
    try {
      const decoded = jwtDecode(token);
      return decoded.user_id;
    } catch (error) {
      console.error("Błąd dekodowania tokena JWT:", error);
      return null;
    }
  };

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
      if (onTripStarted) onTripStarted();
      // setLoading(true);
      // setTimeout(() => window.location.reload(), 100);
    // window.location.reload();
    // const data = await res.json();
    // if (data.trip_id) {
    //   setTripId(data.trip_id); 
    // } else {
    //   alert("Nie udało się rozpocząć trasy (brak trip_id).");
    // }
    } catch (err) {
      console.error("Błąd przy rozpoczynaniu trasy:", err);
      alert("Nie udało się rozpocząć trasy.");
    }
  };

  const sendLocationUpdate = () => {
    if (!tripId) return;

    if (!navigator.geolocation) {
      console.error("Geolokalizacja nie jest dostępna.");
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const { latitude, longitude } = pos.coords;

        try {
          // ⛳ WRÓĆ do wersji z parametrami URL – zgodna z Twoim backendem
          // await fetch(`http://localhost:8000/api/update_location/${tripId}?latitude=${latitude}&longitude=${longitude}`, {
          //   method: "POST",
          //   headers: {
          //     Authorization: `Bearer ${token}`,
          //     "Content-Type": "application/json",
          //   },
          // });
          await fetch(`http://localhost:8000/api/update_location/${tripId}`, {
          method: "POST",
          headers: {
            Authorization: `Bearer ${token}`,
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ latitude, longitude }),
        });
        console.log("Lokalizacja wysłana:", { latitude, longitude });
        } catch (err) {
          console.error("Błąd przy wysyłaniu lokalizacji:", err);
        }
      },
      (err) => {
        console.error("Błąd geolokalizacji:", err);
      }
    );
  };

  const stopTrip = async () => {
    if (!tripId) return;

    clearInterval(intervalRef.current);

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
      setPoints(data.points_earned);
      setAchievements(data.achievements || []);
      setTripId(null);

      if (onTripStopped) onTripStopped();
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
        <>
          <p>📏 Pokonany dystans: {distance.toFixed(2)} km</p>
          <p>🎁 Zdobyte punkty: {points}</p>

          {achievements.length > 0 && (
            <div>
              <p>🏆 Osiągnięcia:</p>
              <ul>
                {achievements.map((a, idx) => (
                  <li key={idx}>✔️ {a}</li>
                ))}
              </ul>
            </div>
          )}
        </>
      )}
    </section>
  );
};

export default RideTracker;
