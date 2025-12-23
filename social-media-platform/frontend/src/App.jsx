import React, { useState, useEffect } from 'react';
import './App.css';
import Auth from './components/Auth';
import Feed from './pages/Feed';
import BotCreator from './components/BotCreator';
import { authAPI } from './services/api';

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkAuth();
  }, []);

  const checkAuth = async () => {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await authAPI.getCurrentUser();
        setCurrentUser(response.data);
        setIsAuthenticated(true);
      } catch (error) {
        localStorage.removeItem('token');
        setIsAuthenticated(false);
      }
    }
    setLoading(false);
  };

  const handleLogin = () => {
    checkAuth();
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setIsAuthenticated(false);
    setCurrentUser(null);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <>
      {isAuthenticated ? (
        <>
          <header className="header">
            <div className="header-content">
              <h1>Social Media Platform</h1>
              <nav>
                <span>Welcome, {currentUser?.username}!</span>
                <button onClick={handleLogout}>Logout</button>
              </nav>
            </div>
          </header>
          <Feed />
          <BotCreator />
        </>
      ) : (
        <Auth onLogin={handleLogin} />
      )}
    </>
  );
}

export default App;
