import React, { createContext, useState, useEffect } from "react";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [token, setToken] = useState(localStorage.getItem("access_token"));
  const [isAuthenticated, setIsAuthenticated] = useState(!!token);

  const login = (newToken) => {
    localStorage.setItem("access_token", newToken);
    setToken(newToken);
    setIsAuthenticated(true);
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setToken(null);
    setIsAuthenticated(false);
  };

  useEffect(() => {
    const stored = localStorage.getItem("access_token");
    if (stored) {
      setToken(stored);
      setIsAuthenticated(true);
    }
  }, []);

  return (
    <AuthContext.Provider value={{ token, isAuthenticated, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
