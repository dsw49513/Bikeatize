import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div>
      <div style={{ textAlign: "center", marginTop: "1rem" }}>
        <img src="/logo2.png" alt="Bikeatize Logo" style={{ width: "150px" }} />
        <br/>
         <img src="/logo3.png" alt="Bikeatize Logo text" style={{ width: "70%", marginTop: "-1.5rem", marginBottom: "1rem" }} />
      </div>
      <div style={{ padding: "2rem", textAlign: "center", marginTop:"5rem" }}>
               <h1 style={{ fontSize:"3rem", textShadow: "0 0 30px rgba(255,255,255,0.8), 0 0px 1px white", transform: "scaleX(-1)"
    }}>🚴‍♂️</h1>

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
