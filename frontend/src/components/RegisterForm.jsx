import React, { useState } from 'react';
import { registerUser } from '../api/authApi';

const RegisterForm = () => {
  const [formData, setFormData] = useState({ name: '', email: '', password: '' });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await registerUser(formData);
      localStorage.setItem('token', data.access_token);
      alert('Rejestracja zakończona sukcesem!');
    } catch (error) {
      alert('Błąd rejestracji: ' + error.response.data.detail);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Rejestracja</h2>
      <input type="text" name="name" placeholder="Imię" onChange={handleChange} required />
      <input type="email" name="email" placeholder="Email" onChange={handleChange} required />
      <input type="password" name="password" placeholder="Hasło" onChange={handleChange} required />
      <button type="submit">Zarejestruj</button>
    </form>
  );
};

export default RegisterForm;
