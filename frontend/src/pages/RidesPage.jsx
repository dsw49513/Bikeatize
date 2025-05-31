import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import TripsHistory from "../components/TripsHistory";
import { getTripHistory, deleteTrip, getTotalDistance } from "../api/tripAPI";
const API_URL = import.meta.env.VITE_API_URL;
const RidesPage = () => {
  const [points, setPoints] = useState(null);
  const [distance, setDistance] = useState(null);
  const [trips, setTrips] = useState([]);
  const navigate = useNavigate();
  const { token, isAuthenticated, userId } = useContext(AuthContext);

  useEffect(() => {
    if (!isAuthenticated || !token) {
      navigate("/login");
      return;
    }

    fetch(`${API_URL}/bt_points/me`, {
      method: "GET",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json",
      },
    })
      .then((res) => res.json())
      .then((data) => {
        setPoints(data.points);
        setDistance(data.total_distance);
      })
      .catch((err) => {
        console.error("Błąd pobierania punktów:", err);
      });

    if (userId) {
      loadTrips();
    }
  }, [isAuthenticated, token, navigate, userId]);

  const loadTrips = async () => {
    try {
      const tripsData = await getTripHistory(userId);
      const distanceData = await getTotalDistance(userId);

      setTrips(tripsData.trips);
      setDistance(distanceData.total_distance || 0);
    } catch (err) {
      console.error("Błąd ładowania tras:", err.message);
    }
  };

  const handleDeleteTrip = async (tripId) => {
    try {
      await deleteTrip(tripId);
      await loadTrips();
    } catch (err) {
      console.error("Błąd usuwania trasy:", err.message);
    }
  };

  return (
    <div style={{ padding: "2rem" }}>
      <h2>🚴 Twoje przejazdy</h2>

      <section>
        <h3>🏅 Punkty / Nagrody:</h3>
        <p>{points !== null ? `${points} pkt` : "Ładowanie..."}</p>
      </section>

      <section>
        <h3>🚴 Dystans całkowity:</h3>
        <p>{typeof distance === "number" ? `${distance.toFixed(2)} km` : "Ładowanie..."}</p>
      </section>

      <section>
        <TripsHistory trips={trips} onDelete={handleDeleteTrip} />
      </section>
    </div>
  );
};

export default RidesPage;