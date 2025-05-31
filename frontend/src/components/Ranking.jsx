import React, { useState, useEffect } from "react";
const API_URL = import.meta.env.VITE_API_URL;

const Ranking = () => {
  const [ranking, setRanking] = useState([]);
  const [filter, setFilter] = useState("global");
  const [loading, setLoading] = useState(true);

  const fetchRanking = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/ranking?filter=${filter}`);
      const data = await response.json();
      if (Array.isArray(data)) {
        setRanking(data);
      } else {
        console.error("Oczekiwano tablicy, ale otrzymano:", data);
        setRanking([]);
      }
    } catch (error) {
      console.error("Błąd podczas pobierania rankingu:", error);
      setRanking([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchRanking();
  }, [filter]);

  return (
    <section className="ranking-card">
      <h2 className="ranking-title">🏆 Ranking użytkowników</h2>

      <div className="ranking-filters">
        <button
          onClick={() => setFilter("global")}
          className={`ranking-filter-button ${filter === "global" ? "active" : ""}`}
        >
          Ogólny
        </button>
        <button
          onClick={() => setFilter("weekly")}
          className={`ranking-filter-button ${filter === "weekly" ? "active" : ""}`}
        >
          Tygodniowy
        </button>
      </div>

      {loading ? (
        <p className="ranking-loading">Ładowanie rankingu...</p>
      ) : ranking.length > 0 ? (
        <table className="ranking-table">
          <thead>
            <tr>
              <th>#</th>
              <th>Użytkownik</th>
              <th>Punkty</th>
            </tr>
          </thead>
          <tbody>
            {ranking.map((user, index) => (
              <tr key={user.name}>
                <td>{index + 1}</td>
                <td>{user.name}</td>
                <td>{user.points}</td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p className="ranking-empty">Brak danych do wyświetlenia.</p>
      )}
    </section>
  );
};

export default Ranking;