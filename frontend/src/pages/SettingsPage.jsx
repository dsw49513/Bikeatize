import React, { useContext, useState } from "react";
import { AuthContext } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";
const API_URL = import.meta.env.VITE_API_URL;


// Max Payne
const QUOTES = [
  "Los drwił ze mnie, ten sam kiepski żart słyszałem już setki razy.",
  "Sceneria się zmieniła, ale reszta była aż nazbyt znajoma.",
  "Nie pamiętam, kiedy ostatni raz czułem coś poza żalem.",
  "Wszystkie te nieudane przejazdy zbierały odsetki.",
  "Tak długo nie widziałem dobrej trasy, że zapomniałem, jak wygląda.",
  "To była najdłuższa próba dotarcia do mety w historii.",
  "W ich twarzach widziałem siebie – ducha własnych błędów.",
  "Żaden kask nie ochroni przed takim bólem.",
  "Każdy dźwięk łańcucha przypominał mi o przeszłości.",
  "Wypełniłem swoje ciało tyloma kilometrami, że tylko to czułem.",
  "Ludzie mówili, że jadę donikąd. Wygląda na to, że już dotarłem.",
  "Wina znów mnie dopadła. Nawet nie zauważyłem, kiedy.",
  "Czułem się, jakbym jechał na ślepo, goniąc horyzont.",
  "Mój świat blakł wokół mnie, zamieniając wszystko w czerń.",
  "Chciałem tylko wrócić na trasę, patrzeć w dal przez kierownicę.",
  "Nie byłem już tym samym rowerzystą co dawniej, a nawet wtedy nie byłem zbyt dobry.",
  "Znowu walczyłem w wyścigu, który nie był mój, z powodów, których nie rozumiałem.",
  "Znowu pomyliłem żal z celem.",
  "Wszystko układało się dobrze, ale nie dla mnie.",
  "Tylko pogarszałem sytuację.",
  "Byłem problemem, który próbował być rozwiązaniem.",
  "Próbowałem grać rolę, gdy kurtyna już dawno opadła.",
  "Została mi tylko pustka, a ona rzadko się przydaje na trasie.",
  "Nikogo nie mogłem uratować, najmniej siebie.",
  "Wracałem na tę samą ścieżkę i wiedziałem, dokąd prowadzi.",
  "Byłem tak daleko za peletonem, że jechałem w innym wyścigu.",
  "Rzeczywistość miała się zaraz roztrzaskać.",
  "To była moja kara. Wciąż popełniać te same błędy.",
  "Stary znajomy – Beznadzieja – znów szeptał mi do ucha."
];

const NO_ANSWERS = [
  "Tutaj musiało się to skończyć.",
  "Czas zejść z trasy, póki jeszcze mogę.",
  "Nic mnie tu już nie trzyma.",
  "Szczęście się skończyło.",
  "Przedstawienie dobiegło końca.",
  "Może tak właśnie musiało być.",
  "Muszę się poddać.",
  "Cena była zbyt wysoka.",
  "Lepiej żyć złudzeniem niż zmierzyć się z prawdą.",
  "Zawiodłem już wystarczająco wielu ludzi.",
  "Byłem tylko cieniem dawnego siebie.",
  "Zainwestowałem za dużo w coś, co nie miało zwrotu.",
  "Ciało bolało. Byłem już za stary na ten wyścig.",
  "Byłem tu już zbyt wiele razy."
];

const YES_ANSWERS = [
  "Może jeszcze mam szansę wrócić na trasę.",
  "Ale nie mogę się teraz poddać.",
  "Zaszedłem już za daleko.",
  "To nie czas na użalanie się nad sobą.",
  "Nie ma już odwrotu.",
  "Muszę to dokończyć.",
  "Jestem już za głęboko w tym wyścigu.",
  "Nie mogę wybrać łatwej drogi.",
  "To mój bałagan. Muszę go posprzątać.",
  "Zbyt wiele pytań pozostało bez odpowiedzi.",
  "Za dużo jest do stracenia.",
  "Muszę jechać dalej.",
  "Wiedziałem, że nie mogę się wycofać.",
  "To nie dotyczy tylko mnie.",
  "Nie mam wyboru, muszę naciskać dalej.",
  "To nie czas na wątpliwości."
];


const SettingsPage = () => {
  const { logout } = useContext(AuthContext); 
  const navigate = useNavigate();
  const [showModal, setShowModal] = useState(false);
  const [quote, setQuote] = useState("");
  const [noAnswer, setNoAnswer] = useState("");
  const [yesAnswer, setYesAnswer] = useState("");
  const [loggingOut, setLoggingOut] = useState(false);

  const handleLogout = async () => {
    setLoggingOut(true);
    try {
      
      const response = await fetch(`${API_URL}/logout`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("access_token")}`, 
        },
      });

      if (response.ok) {
      logout();
      navigate("/login");
    } else {
      // Jeśli błąd dotyczy wygasłego tokena, wyloguj lokalnie
      const err = await response.text();
      if (err.includes("Signature has expired")) {
        logout();
        navigate("/login");
        return;
      }
      console.error("Nie udało się usunąć refresh tokena:", err);
      alert("Wystąpił problem podczas wylogowywania.");
    }
    } catch (error) {
      console.error("Błąd podczas wylogowywania:", error);
      alert("Nie udało się połączyć z serwerem.");
    }
  };
   const handleLogoutClick = () => {
 
      setQuote(QUOTES[Math.floor(Math.random() * QUOTES.length)]);
      setNoAnswer(NO_ANSWERS[Math.floor(Math.random() * NO_ANSWERS.length)]);
      setYesAnswer(YES_ANSWERS[Math.floor(Math.random() * YES_ANSWERS.length)]);
      setShowModal(true);
    };

    const handleCancel = () => {
      setShowModal(false);
    };

    const handleConfirm = () => {
      setShowModal(false);
      handleLogout();
    };
  return (
    <div style={{ padding: "2rem", textAlign: "center" }}>
      <h2>⚙️ Ustawienia</h2>
      <p>Twoje konto</p>
      <button
        onClick={handleLogoutClick}
        style={{
          backgroundColor: "#4caf50", 
          color: "#ffffff",
          border: "none",
          borderRadius: "5px",
          padding: "0.5rem 1rem",
          fontSize: "1rem",
          cursor: "pointer",
          transition: "background-color 0.3s ease",
        }}
        disabled={loggingOut}
      >
        Wyloguj się
      </button>

      {showModal && (
        <div style={{
          position: "fixed",
          top: 0, left: 0, right: 0, bottom: 0,
          background: "rgba(0,0,0,0.85)",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          zIndex: 9999
        }}>
          <div style={{
            background: "#222",
            color: "#fff",
            padding: "2rem",
            borderRadius: "10px",
            maxWidth: "400px",
            boxShadow: "0 0 30px #000",
            textAlign: "center"
          }}>
            <p style={{ fontStyle: "italic", marginBottom: "2rem" }}>{quote}</p>
            <button
              onClick={handleCancel}
              style={{
                background: "#333",
                color: "#fff",
                border: "1px solid #fff",
                borderRadius: "5px",
                padding: "0.5rem 1rem",
                marginRight: "1rem",
                marginBottom:"2rem",
                cursor: "pointer"
              }}
            >
              {yesAnswer}
            </button>
            <button
              onClick={handleConfirm}
              style={{
                background: "#800020",
                color: "#fff",
                border: "none",
                borderRadius: "5px",
                padding: "0.5rem 1rem",
                cursor: "pointer"
              }}
              disabled={loggingOut}
            >
              {noAnswer}
            </button>
          </div>
        </div>
      )}
    </div>
  );
};

export default SettingsPage;