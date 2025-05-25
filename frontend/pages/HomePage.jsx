// frontend/src/pages/HomePage.jsx

import React, { useState } from "react";
import { Link } from "react-router-dom";
import UserForm from "../components/UserForm";
import UserList from "../components/UserList";

const HomePage = () => {
  const [refresh, setRefresh] = useState(false);

  // Funkcja przeładowująca listę użytkowników po dodaniu nowego
  const triggerRefresh = () => setRefresh(!refresh);

  return (
    <div>
      <h1>Strona główna</h1>

      <nav style={{ marginBottom: "20px" }}>
        <Link to="/login">Logowanie</Link> |{" "}
        <Link to="/register">Rejestracja</Link>
      </nav>

      <h2>Dodaj użytkownika</h2>
      <UserForm onUserAdded={triggerRefresh} />

      <h2>Lista użytkowników</h2>
      <UserList key={refresh} />
    </div>
  );
};

export default HomePage;
