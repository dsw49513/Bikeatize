// frontend/src/pages/HomePage.jsx

import React from "react";
import { Link } from "react-router-dom";

const HomePage = () => {
  return (
    <div>
      <h1>Strona główna</h1>
      <nav>
        <Link to="/login">Logowanie</Link> | <Link to="/register">Rejestracja</Link>
      </nav>
    </div>
  );
};

export default HomePage;
