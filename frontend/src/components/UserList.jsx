import React, { useEffect, useState } from 'react';
import { getUsers } from '../api/userApi';

const UserList = () => {
  const [users, setUsers] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    getUsers()
      .then((res) => {
        if (res?.data && Array.isArray(res.data)) {
          setUsers(res.data);
        } else {
          throw new Error('Nieprawidłowy format danych z backendu');
        }
      })
      .catch((err) => {
        console.error('Błąd pobierania danych:', err);
        setError('Wystąpił problem z pobieraniem użytkowników.');
      });
  }, []);

  if (error) {
    return <div style={{ color: 'red' }}>{error}</div>;
  }

  return (
    <div>
      <h2>Lista użytkowników</h2>
      <ul>
        {users.length === 0 ? (
          <li>Brak użytkowników.</li>
        ) : (
          users.map((user) => (
            <li key={user._id}>
              {user.name} – {user.email}
            </li>
          ))
        )}
      </ul>
    </div>
  );
};

export default UserList;
