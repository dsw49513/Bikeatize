import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

// Znajdowanie elementu <div id="root"> w pliku public/index.html
const root = ReactDOM.createRoot(document.getElementById('root'));

// Renderowanie głównego komponentu <App />
root.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
