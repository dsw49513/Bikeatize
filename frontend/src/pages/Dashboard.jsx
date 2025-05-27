import React, { useEffect, useState } from "react";

const Dashboard = () => {
  const [location, setLocation] = useState(null);
  const [error, setError] = useState(null);
  const [points, setPoints] = useState(null);
  const [distance, setDistance] = useState(null);

  useEffect(() => {
    // Pobranie lokalizacji użytkownika
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

    // TODO: pobierz punkty i dystans z backendu po zalogowaniu
    // fetchUserData();
  }, []);

  return (
    <div style={{ padding: "2rem" }}>
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
        <p>{points !== null ? `${points} pkt` : "Brak danych"}</p>
      </section>

      <section>
        <h3>🚴 Dystans całkowity:</h3>
        <p>{distance !== null ? `${distance} km` : "Brak danych"}</p>
      </section>

      <section style={{ marginTop: "2rem" }}>
        <h3>🗺️ Mapa (wkrótce)</h3>
        <div style={{ width: "100%", height: "300px", backgroundColor: "#eee", textAlign: "center", lineHeight: "300px" }}>
          [tutaj będzie mapa]
        </div>
      </section>
    </div>
  );
};

export default Dashboard;
