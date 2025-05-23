import React, { useState } from 'react';
import UserForm from '../components/UserForm';
import UserList from '../components/UserList';

const HomePage = () => {
  const [refresh, setRefresh] = useState(false);

  const triggerRefresh = () => setRefresh(!refresh);

  return (
    <div>
      <h1>Hello from HomePage!</h1>
      <UserForm onUserAdded={triggerRefresh} />
      <UserList key={refresh} />
    </div>
  );
};

export default HomePage;
