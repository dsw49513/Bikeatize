import React, { useState, useEffect, useContext } from 'react';
import { AuthContext } from '../context/AuthContext';
import { getTotalKilometers, startRide } from '../api/userApi';

const Home = () => {
  const { token } = useContext(AuthContext);
  const [totalKilometers, setTotalKilometers] = useState(0);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchKilometers = async () => {
      try {
        const data = await getTotalKilometers(token);
        setTotalKilometers(data.total_distance_km);
      } catch (err) {
        setError('Błąd kilometrów');
      }
    };

    fetchKilometers();
  }, [token]);

  const handleStartRide = async () => {
    try {
      await startRide(token);
      alert('Start');
    } catch (err) {
      setError('Błąd startu');
    }
  };

  return (
    <div>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      <p>Łącznie przejechane kilometry: {totalKilometers} km</p>
      <button onClick={handleStartRide}>Start</button>
    </div>
  );
};

export default Home;