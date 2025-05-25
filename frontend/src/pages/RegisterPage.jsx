import React, { useState } from "react";

const RegisterPage = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  console.log(">>> Załadowano RegisterPage"); // TEST

  const handleRegister = async (e) => {
  e.preventDefault();
  console.log("Kliknięto Zarejestruj"); // DEBUG

  try {
    const res = await fetch("http://localhost:8000/api/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, email, password }),
    });

    const data = await res.json();
    console.log("Rejestracja - odpowiedź serwera:", data);

    if (res.ok) {
      alert("Użytkownik zarejestrowany!");
    } else {
      alert("Błąd: " + (data.detail || JSON.stringify(data)));
    }
  } catch (err) {
    console.error("Błąd połączenia z serwerem:", err);
    alert("Błąd połączenia z serwerem");
  }
};


  return (
    <div>
      <h2>Rejestracja</h2>
      <form onSubmit={handleRegister}>
        <input
          type="text"
          placeholder="Nazwa użytkownika"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
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
        <button type="submit">Zarejestruj</button>
      </form>
    </div>
  );
};

export default RegisterPage;
