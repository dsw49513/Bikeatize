import React, { useState } from "react";
import { useNavigate } from "react-router-dom"; // ✅ dodano

const LoginPage = () => {
  const [email, setEmail] = useState(""); 
  const [password, setPassword] = useState("");
  const navigate = useNavigate(); // ✅ użycie hooka do przekierowań

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
        alert("Zalogowano! Token: " + data.access_token);
        navigate("/dashboard"); // ✅ przekierowanie po zalogowaniu
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
