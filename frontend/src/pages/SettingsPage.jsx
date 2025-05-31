import React, { useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
const API_URL = import.meta.env.VITE_API_URL;
const SettingsPage = () => {
  const { logout } = useContext(AuthContext); 
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      
      const response = await fetch(`${API_URL}/logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`, 
        },
      });

      if (response.ok) {
      logout();
      navigate("/login");
    } else {
      // Jeśli błąd dotyczy wygasłego tokena, wyloguj lokalnie
      const err = await response.text();
      if (err.includes("Signature has expired")) {
        logout();
        navigate("/login");
        return;
      }
      console.error("Nie udało się usunąć refresh tokena:", err);
      alert("Wystąpił problem podczas wylogowywania.");
    }
    } catch (error) {
      console.error("Błąd podczas wylogowywania:", error);
      alert("Nie udało się połączyć z serwerem.");
    }
  };

  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h2>⚙️ Ustawienia</h2>
      <p>Twoje konto</p>
      <button
        onClick={handleLogout}
        style={{
          backgroundColor: "#4caf50", 
          color: "#ffffff",
          border: "none",
          borderRadius: "5px",
          padding: "0.5rem 1rem",
          fontSize: "1rem",
          cursor: "pointer",
          transition: "background-color 0.3s ease",
        }}
      >
        Wyloguj się
      </button>
    </div>
  );
};

export default SettingsPage;