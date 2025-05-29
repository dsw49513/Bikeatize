import React from "react";

const TripsHistory = ({ trips, onDelete }) => {
  if (!trips || trips.length === 0) {
    return (
      <section>
        <h3>🛣️ Historia tras:</h3>
        <p>Brak zapisanych tras.</p>
      </section>
    );
  }

  return (
    <section>
      <h3>🛣️ Historia tras:</h3>
      <ul>
        {trips.map((trip) => (
          <li key={trip.id}>
            <strong>Trasa #{trip.id}</strong> | Start:{" "}
            {new Date(trip.start_time).toLocaleString()} | Koniec:{" "}
            {trip.end_time
              ? new Date(trip.end_time).toLocaleString()
              : "Trwa"}{" "}
            | Dystans: {trip.total_distance_km.toFixed(2)} km
            <button
              onClick={() => onDelete(trip.trip_id)}
              style={{ marginLeft: "1rem" }}
            >
              Usuń
            </button>
          </li>
        ))}
      </ul>
    </section>
  );
};

export default TripsHistory;
