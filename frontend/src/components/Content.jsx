import React, { useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import HomePage2 from '../pages/HomePage2';
import LoginPage from '../pages/LoginPage';

const Content = () => {
  const { isLoggedIn } = useContext(AuthContext);

  return isLoggedIn ? <HomePage2 /> : <LoginPage />;
};

export default Content;