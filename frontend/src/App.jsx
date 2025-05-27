import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthContextProvider } from './context/AuthContext';
import Content from './components/Content';
import LoginPage from './pages/LoginPage';
import UserForm from './components/UserForm';

const App = () => {
  return (
    <AuthContextProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Content />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<UserForm />} />
        </Routes>
      </Router>
    </AuthContextProvider>
  );
};

export default App;
