import React, { useState, useEffect } from 'react';
import { getUsers } from '../api/userApi';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
  console.log("🔥 Pobieram użytkowników...");
  getUsers()
    .then((res) => {
      console.log("✅ Odpowiedź API:", res.data);
      setUsers(Array.isArray(res) ? res : []); // ✅ poprawka
    })
    .catch((err) => {
      console.error("❌ Błąd API:", err);
      setError("Błąd pobierania użytkowników.");
    });
}, []);


  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Lista użytkowników</h2>
      <ul>
        {users.map((user) => (
          <li key={user._id}>{user.name} – {user.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default UserList;
