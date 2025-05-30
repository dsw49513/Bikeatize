import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div>
      <div style={{ textAlign: "center", marginTop: "1rem" }}>
        <img src="/logo2.png" alt="Bikeatize Logo" style={{ width: "150px", marginBottom: "1rem" }} />
      </div>
      <div style={{ padding: "2rem", textAlign: "center" }}>
        <h1>🚴‍♂️ Bikeatize</h1>
        <p>Aplikacja dla entuzjastów jazdy na rowerze</p>
      </div>
      <div style={{ textAlign: "center", marginTop: "1rem" }}>
        <nav>
          <Link to="/login">Logowanie</Link> | <Link to="/register">Rejestracja</Link>
        </nav>
      </div>
    </div>
  );
};

export default HomePage;
