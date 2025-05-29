import React, { useState, useEffect } from "react";

const Ranking = () => {
  const [ranking, setRanking] = useState([]);
  const [filter, setFilter] = useState("global");
  const [loading, setLoading] = useState(true);

  const fetchRanking = async () => {
    setLoading(true);
    try {
      const response = await fetch(`http://localhost:8000/api/ranking?filter=${filter}`);
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
    <section>
      <h2>🏆 Ranking użytkowników</h2>

      <div style={{ marginBottom: "1rem", display: "flex", gap: "1rem" }}>
        <button
          onClick={() => setFilter("global")}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: filter === "global" ? "#007bff" : "#f0f0f0",
            color: filter === "global" ? "#fff" : "#000",
            border: "1px solid #ccc",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Ogólny
        </button>
        <button
          onClick={() => setFilter("weekly")}
          style={{
            padding: "0.5rem 1rem",
            backgroundColor: filter === "weekly" ? "#007bff" : "#f0f0f0",
            color: filter === "weekly" ? "#fff" : "#000",
            border: "1px solid #ccc",
            borderRadius: "5px",
            cursor: "pointer",
          }}
        >
          Tygodniowy
        </button>
      </div>


      {loading ? (
        <p>Ładowanie rankingu...</p>
      ) : ranking.length > 0 ? (
        <table>
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
        <p>Brak danych do wyświetlenia.</p>
      )}
    </section>
  );
};

export default Ranking;