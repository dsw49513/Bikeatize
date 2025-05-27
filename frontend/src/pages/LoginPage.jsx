import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../context/AuthContext"; // ✅ import

const LoginPage = () => {
  const [email, setEmail] = useState(""); 
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const { login } = useContext(AuthContext); // ✅ użycie kontekstu

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
        login(data.access_token); // ✅ ustaw token przez kontekst
        navigate("/dashboard");
      } else {
        alert("Błąd logowania");
      }
    } catch (err) {
      alert("Błąd serwera");
    }
  };

  return (
    <div>
      <h2>Logowanie</h2>
      <form onSubmit={handleLogin}>
        <input
          type="email"
          placeholder="E-mail"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Hasło"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">Zaloguj</button>
      </form>
    </div>
  );
};

export default LoginPage;
