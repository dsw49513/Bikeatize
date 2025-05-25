import React, { useState } from 'react';
import { loginUser } from '../api/authApi';

const LoginForm = () => {
  const [credentials, setCredentials] = useState({ email: '', password: '' });

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await loginUser(credentials);
      localStorage.setItem('token', data.access_token);
      alert('Zalogowano pomyślnie!');
    } catch (error) {
      alert('Błąd logowania: ' + error.response.data.detail);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Logowanie</h2>
      <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
      <input type="password" name="password" placeholder="Hasło" onChange={handleChange} required />
      <button type="submit">Zaloguj</button>
    </form>
  );
};

export default LoginForm;
