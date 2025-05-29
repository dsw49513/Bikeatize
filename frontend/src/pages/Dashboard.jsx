import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import TripsHistory from "../components/TripsHistory";
import RideTracker from "../components/RideTracker";
import { getTripHistory, deleteTrip, getTotalDistance } from "../api/tripAPI";

const Dashboard = () => {
  const [location, setLocation] = useState(null);
  const [error, setError] = useState(null);
  const [points, setPoints] = useState(null);
  const [distance, setDistance] = useState(null);
  const [trips, setTrips] = useState([]);
  const navigate = useNavigate();
  const { token, isAuthenticated, logout, userId } = useContext(AuthContext);

  useEffect(() => {
    if (!isAuthenticated || !token) {
      navigate("/login");
      return;
    }

    // 📍 Lokalizacja przeglądarki
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

    // 🔐 Fetch punktów z backendu
    fetch("http://localhost:8000/api/bt_points/me", {
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

    // 📦 Pobranie historii tras i dystansu
    if (userId) {
      loadTrips();
    }
  }, [isAuthenticated, token, navigate, userId]);

const loadTrips = async () => {
  try {
    const tripsData = await getTripHistory(userId);
    console.log("Dane z historii tras:", tripsData);

    const distanceData = await getTotalDistance(userId);
    console.log("Dane z dystansu:", distanceData);

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

  // 🧭 Marker domyślny (ikonka lokalizacji)
  const markerIcon = new L.Icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
  });

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

      {location && (
        <section>
          <h3>🗺️ Mapa</h3>
          <MapContainer
            center={[location.lat, location.lng]}
            zoom={13}
            style={{ height: "300px", width: "100%" }}
          >
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
              attribution="&copy; OpenStreetMap"
            />
            <Marker position={[location.lat, location.lng]} icon={markerIcon}>
              <Popup>Tu jesteś!</Popup>
            </Marker>
          </MapContainer>
        </section>
      )}

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

      <section>
        <RideTracker onTripStopped={loadTrips} />
      </section>
    </div>
  );
};

export default Dashboard;
