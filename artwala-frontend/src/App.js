import React from 'react';
import './App.css';
import Dashboard from './components/Dashboard';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>ARTWALA - Art Marketplace</h1>
        <p>Full-stack Django + React Application</p>
      </header>
      <main className="App-main">
        <Dashboard />
      </main>
    </div>
  );
}

export default App;
