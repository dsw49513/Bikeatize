
import React, { useState, useContext } from "react";
import { useNavigate, Link } from "react-router-dom";
import { AuthContext } from "../context/AuthContext";

const LoginPage = () => {
  const [email, setEmail] = useState(""); 
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login } = useContext(AuthContext);

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const res = await fetch("http://localhost:8000/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });

      if (res.ok) {
        const data = await res.json();
        login(data.access_token);
        navigate("/dashboard");
      } else {
        const errorText = await res.text();
        console.error("Błąd backendu:", errorText);
        alert("Błąd logowania: " + errorText);
      }
    } catch (err) {
      console.error("Błąd połączenia z backendem:", err);
      alert("Błąd połączenia z serwerem");

    }
  };

  return (

    <div style={{ padding: "2rem", maxWidth: "400px", margin: "0 auto" }}>
      <div style={{ textAlign: "center", marginTop: "1rem" }}>
        <img src="/logo2.png" alt="Bikeatize Logo" style={{ width: "150px", marginBottom: "1rem" }} />
      </div>
      <h2>Logowanie</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
          style={{ display: "block", width: "100%", marginBottom: "1rem", boxSizing: "border-box" }}

        />
        <input
          type="password"
          placeholder="Hasło"
          value={password}
          onChange={(e) => setPassword(e.target.value)}

          required
          style={{ display: "block", width: "100%", marginBottom: "1rem" , boxSizing: "border-box"}}
        />
        <button type="submit" style={{
          width: "100%",
          boxSizing: "border-box",
          padding: "0.5rem",
          marginBottom: "1rem"
        }}>Zaloguj</button>
      </form>

      <div style={{ marginTop: "1.5rem", textAlign: "center" }}>
        <p>
          Nie masz jeszcze konta? <Link to="/register">Zarejestruj się</Link>
        </p>
        <p>
          <Link to="/">← Powrót na stronę główną</Link>
        </p>
      </div>

    </div>
  );
};


export default LoginPage;

