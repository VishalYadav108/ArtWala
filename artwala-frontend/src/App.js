import React, { useState } from 'react';
import './App.css';
import UserDashboard from './components/UserDashboard';
import ArtistDashboard from './components/ArtistDashboard';

function App() {
  const [userType, setUserType] = useState('user'); // 'user' or 'artist'

  return (
    <div className="App">
      {/* Navigation */}
      <nav style={{ 
        padding: '10px 20px', 
        backgroundColor: '#f8f9fa', 
        borderBottom: '1px solid #ddd',
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center'
      }}>
        <h2 style={{ margin: 0, color: '#007bff' }}>ArtWala</h2>
        <div>
          <button 
            onClick={() => setUserType('user')}
            style={{ 
              backgroundColor: userType === 'user' ? '#007bff' : '#6c757d',
              color: 'white', 
              border: 'none', 
              padding: '8px 16px', 
              marginRight: '10px',
              borderRadius: '3px',
              cursor: 'pointer'
            }}
          >
            User View
          </button>
          <button 
            onClick={() => setUserType('artist')}
            style={{ 
              backgroundColor: userType === 'artist' ? '#007bff' : '#6c757d',
              color: 'white', 
              border: 'none', 
              padding: '8px 16px',
              borderRadius: '3px',
              cursor: 'pointer'
            }}
          >
            Artist View
          </button>
        </div>
      </nav>

      {/* Main Content */}
      {userType === 'user' ? <UserDashboard /> : <ArtistDashboard />}
    </div>
  );
}

export default App;
