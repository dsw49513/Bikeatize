import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const Dashboard = () => {
  const [location, setLocation] = useState(null);
  const [error, setError] = useState(null);
  const [points, setPoints] = useState(null);
  const [distance, setDistance] = useState(null);
  const navigate = useNavigate();

  const { token, isAuthenticated, logout } = useContext(AuthContext);

  useEffect(() => {
    if (!isAuthenticated || !token) {
      navigate("/login");
      return;
    }

    // 📍 Lokalizacja
    navigator.geolocation.getCurrentPosition(
      (position) => {
        setLocation({
          lat: position.coords.latitude,
          lng: position.coords.longitude,
        });
      },
      (err) => {
        setError("Nie udało się uzyskać lokalizacji.");
        console.error(err);
      }
    );

    // 🎯 Fetch punktów
    fetch("http://localhost:8000/bt_points/me", {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setPoints(data.points); // zależnie od struktury
        setDistance(data.total_distance);
      })
      .catch((err) => {
        console.error("Błąd pobierania punktów:", err);
      });
  }, [isAuthenticated, token, navigate]);

  return (
    <div style={{ padding: "2rem" }}>
      <button onClick={logout}>Wyloguj się</button>

      <h2>🎯 Dashboard użytkownika</h2>

      <section>
        <h3>📍 Twoja lokalizacja:</h3>
        {location ? (
          <p>
            Szerokość: {location.lat.toFixed(4)}, Długość: {location.lng.toFixed(4)}
          </p>
        ) : error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : (
          <p>Trwa pobieranie lokalizacji...</p>
        )}
      </section>

      <section>
        <h3>🏅 Punkty / Nagrody:</h3>
        <p>{points !== null ? `${points} pkt` : "Ładowanie..."}</p>
      </section>

      <section>
        <h3>🚴 Dystans całkowity:</h3>
        <p>{distance !== null ? `${distance} km` : "Ładowanie..."}</p>
      </section>
    </div>
  );
};

export default Dashboard;
