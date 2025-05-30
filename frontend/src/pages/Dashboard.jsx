import React, { useEffect, useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet";
import RideTracker from "../components/RideTracker";
import TripsHistory from "../components/TripsHistory";
import { getTripHistory, deleteTrip, getTotalDistance } from "../api/tripAPI";

const Dashboard = () => {
  const [location, setLocation] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const [trips, setTrips] = useState([]); 
  const [distance, setDistance] = useState(0); 
  const [points, setPoints] = useState(null);
  const { token, isAuthenticated, userId, logout } = useContext(AuthContext);

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
  }, [isAuthenticated, token, navigate]);
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
  // 🧭 Marker domyślny (ikonka lokalizacji)
  const markerIcon = new L.Icon({
    iconUrl: "https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png",
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
  });

  return (
    <div style={{ padding: "2rem" }}>
      
     <section>
      <RideTracker onTripStopped={loadTrips}/>
      </section>
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

      
    </div>
  );
};

export default Dashboard;