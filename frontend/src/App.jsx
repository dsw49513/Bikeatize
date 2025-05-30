import React, { useContext } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";
import Ranking from "./components/Ranking";
import Dashboard from "./pages/Dashboard";
import RidesPage from "./pages/RidesPage";
import SettingsPage from "./pages/SettingsPage"; 

import Navbar from "./components/Navbar"; 
import { AuthContext } from "./context/AuthContext";
import "./App.css";

const App = () => {
  const { isAuthenticated } = useContext(AuthContext); 

  return (
    <Router>
      <div style={{ paddingBottom: "50px" }}> 
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/rides" element={<RidesPage />} />
          <Route path="/ranking" element={<Ranking />} />
          <Route path="/settings" element={<SettingsPage />} /> {/* Nowa trasa */}
        </Routes>
      </div>
      {isAuthenticated && <Navbar />}
    </Router>
  );
};

export default App;