
import React, { createContext, useState, useEffect } from "react";
import { jwtDecode } from "jwt-decode";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("access_token"));
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);
  const [userId, setUserId] = useState(() => {
    const stored = localStorage.getItem("access_token");
    if (stored) {
      try {
        return jwtDecode(stored).user_id;
      } catch (e) {
        console.error("Błąd dekodowania JWT:", e);
        return null;
      }
    }
    return null;
  });

  const login = (newToken) => {
    localStorage.setItem("access_token", newToken);
    setToken(newToken);
    setIsAuthenticated(true);
    try {
      const decoded = jwtDecode(newToken);
      setUserId(decoded.user_id);
    } catch (e) {
      console.error("Błąd dekodowania JWT po loginie:", e);
    }
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setIsAuthenticated(false);
    setUserId(null);
  };

  useEffect(() => {
    const stored = localStorage.getItem("access_token");
    if (stored) {
      setToken(stored);
      setIsAuthenticated(true);
      try {
        setUserId(jwtDecode(stored).user_id);
      } catch (e) {
        console.error("Błąd dekodowania JWT w useEffect:", e);
      }
    }
  }, []);

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, login, logout, userId }}>
      {children}
    </AuthContext.Provider>
  );
};

