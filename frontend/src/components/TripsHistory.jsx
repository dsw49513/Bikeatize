import React from "react";
import DeleteIcon from "@mui/icons-material/Delete";
import StraightenIcon from "@mui/icons-material/Straighten";
import ArrowForwardIcon from "@mui/icons-material/ArrowForward"; // Ikona startu
import FlagIcon from "@mui/icons-material/Flag"; // Ikona mety

const TripsHistory = ({ trips, onDelete }) => {
  if (!trips || trips.length === 0) {
    return (
      <section className="card">
        <h3>🛣️ Historia tras:</h3>
        <p>Brak zapisanych tras.</p>
      </section>
    );
  }

  const handleDelete = (tripId) => {
    if (window.confirm("Czy na pewno chcesz usunąć tę trasę?")) {
      onDelete(tripId);
    }
  };

  return (
    <section className="card">
      <h3>🛣️ Historia tras:</h3>
      <ul className="trips-history">
        {trips.map((trip, index) => (
          <React.Fragment key={trip.trip_id}>
            <li style={{ display: "flex", alignItems: "center", gap: "1rem" }}>
              <div style={{ display: "flex", flexDirection: "column", gap: "0.5rem" }}>
                <div style={{ display: "flex", alignItems: "center" }}>
                  <StraightenIcon style={{ marginRight: "0.5rem", color: "#4caf50" }} />
                  Dystans: {trip.total_distance_km.toFixed(2)} km
                </div>
                <div style={{ display: "flex", alignItems: "center" }}>
                  <ArrowForwardIcon style={{ marginRight: "0.5rem", color: "#4caf50" }} />
                  Start: {new Date(trip.start_time).toLocaleString()}
                </div>
                <div style={{ display: "flex", alignItems: "center" }}>
                  <FlagIcon style={{ marginRight: "0.5rem", color: "#4caf50" }} />
                  Koniec: {trip.end_time
                    ? new Date(trip.end_time).toLocaleString()
                    : "Trwa"}
                </div>
              </div>
              <button
                onClick={() => handleDelete(trip.trip_id)}
                style={{
                  backgroundColor: "transparent",
                  border: "none",
                  color: "#ff4d4d", 
                  cursor: "pointer",
                  fontSize: "1.2rem",
                  marginLeft: "auto",
                }}
              >
                <DeleteIcon />
              </button>
            </li>
            {index < trips.length - 1 && (
              <hr style={{ border: "none", borderTop: "1px solid #ccc", margin: "1rem 0" }} />
            )}
          </React.Fragment>
        ))}
      </ul>
    </section>
  );
};

export default TripsHistory;