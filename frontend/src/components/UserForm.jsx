import React, { useState } from 'react';
import { createUser } from '../api/userApi';

const UserForm = ({ onUserAdded }) => {
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await createUser({ name, email });
      setName('');
      setEmail('');
      onUserAdded();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <h2>Dodaj użytkownika</h2>
      <input
        type="text"
        placeholder="Imię"
        value={name}
        onChange={(e) => setName(e.target.value)}
        required
      />
      <input
        type="email"
        placeholder="E-mail"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <button type="submit">Dodaj</button>
    </form>
  );
};

export default UserForm;
