import React from 'react';

const Navbar = () => {
  return (
    <nav style={{ position: 'fixed', bottom: 0, width: '100%', background: '#ccc' }}>
      <ul style={{ display: 'flex', justifyContent: 'space-around', padding: 0 }}>
        <li><a href="/home">Start</a></li>
        <li><a href="/rides">Przejazdy</a></li>
        <li><a href="/ranking">Ranking</a></li>
      </ul>
    </nav>
  );
};

export default Navbar;