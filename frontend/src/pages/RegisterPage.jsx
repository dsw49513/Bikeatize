import React, { useState } from "react";
import { useNavigate, Link } from "react-router-dom";

const RegisterPage = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:8000/api/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name: username, email, password }),
      });

      if (res.ok) {
        alert("Rejestracja zakończona sukcesem! Zaloguj się.");
        navigate("/login");
      } else {
        alert("Błąd rejestracji");
      }
    } catch (err) {
      alert("Błąd połączenia z serwerem");
    }
  };

  return (
    <div style={{ padding: "2rem", maxWidth: "400px", margin: "0 auto" }}>
      <div style={{ textAlign: "center", marginTop: "1rem" }}>
        <img src="/logo2.png" alt="Bikeatize Logo" style={{ width: "150px", marginBottom: "1rem" }} />
      </div>
      <h2>Rejestracja</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Nazwa użytkownika"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: "1rem" }}
        />
        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: "1rem" }}
        />
        <input
          type="password"
          placeholder="Hasło"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: "1rem" }}
        />
        <button type="submit" style={{ width: "100%" }}>Zarejestruj się</button>
      </form>

      <div style={{ marginTop: "1.5rem", textAlign: "center" }}>
        <p>
          Masz już konto? <Link to="/login">Zaloguj się</Link>
        </p>
        <p>
          <Link to="/">← Powrót na stronę główną</Link>
        </p>
      </div>
    </div>
  );
};

export default RegisterPage;
