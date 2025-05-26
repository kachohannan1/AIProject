import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { FiSun, FiMoon, FiSettings, FiHeart, FiClock, FiArrowRight, FiX } from 'react-icons/fi';
import './ChatApp.css';

const ChatApp = () => {
  const [darkMode, setDarkMode] = useState(false);
  const [currentUser, setCurrentUser] = useState(null);
  const [showAuthModal, setShowAuthModal] = useState(false);
  const [isLoginView, setIsLoginView] = useState(true);
  const [activeTab, setActiveTab] = useState('chat');
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: ''
  });
  const [error, setError] = useState('');
  const [messages, setMessages] = useState([]);
  const [inputMessage, setInputMessage] = useState('');
  const [suggestions, setSuggestions] = useState([]);

  useEffect(() => {
    const token = localStorage.getItem('authToken');
    const userStr = localStorage.getItem('currentUser');
    if (token && userStr) {
      setCurrentUser(JSON.parse(userStr));
    }
  }, []);

  useEffect(() => {
    setMessages([{ text: 'What Can I help with?', sender: 'bot' }]);
  }, []);

  useEffect(() => {
    if (inputMessage.trim() === '') {
      setSuggestions([]);
      return;
    }

    const fetchSuggestions = async () => {
      try {
        const token = localStorage.getItem('authToken');
        const response = await axios.post(
          'http://localhost:8001/predict/',
          { message: inputMessage },
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );
        setSuggestions(response.data.suggestions || []);
      } catch (error) {
        console.error('Error fetching suggestions:', error);
      }
    };

    const debounce = setTimeout(fetchSuggestions, 300);

    return () => clearTimeout(debounce);
  }, [inputMessage]);

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignup = async (e) => {
    e.preventDefault();
    setError('');

    try {
      await axios.post('http://localhost:8000/api/register/', {
        username: formData.username,
        email: formData.email,
        password: formData.password,
      });

      setIsLoginView(true);
      setFormData({ username: '', email: '', password: '' });
    } catch (err) {
      if (err.response && err.response.data) {
        setError(JSON.stringify(err.response.data));
      } else {
        setError('Signup failed. Please try again.');
      }
    }
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await axios.post('http://localhost:8000/api/login/', {
        email: formData.email,
        password: formData.password,
      });

      const { token, user } = response.data;

      localStorage.setItem('authToken', token);
      localStorage.setItem('currentUser', JSON.stringify(user));

      setCurrentUser(user);
      setShowAuthModal(false);
      setFormData({ username: '', email: '', password: '' });
    } catch (err) {
      if (err.response && err.response.data) {
        setError(err.response.data.error || 'Login failed');
      } else {
        setError('Login failed. Please try again.');
      }
    }
  };

  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem('authToken');
    localStorage.removeItem('currentUser');
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!currentUser) {
      setError('You must be logged in to send messages.');
      setShowAuthModal(true);
      setIsLoginView(true);
      return;
    }

    if (inputMessage.trim()) {
      const userMsg = { text: inputMessage, sender: 'user' };
      setMessages((prev) => [...prev, userMsg]);
      setInputMessage('');
      setSuggestions([]);

      try {
        const token = localStorage.getItem('authToken');

        const res = await fetch('http://localhost:8001/predict/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Token ${token}`,
          },
          body: JSON.stringify({ message: inputMessage }),
        });

        const data = await res.json();
        const botMsg = { text: data.response, sender: 'bot' };
        setMessages((prev) => [...prev, botMsg]);
      } catch (err) {
        setMessages((prev) => [
          ...prev,
          { text: "Sorry, I couldn't connect to the server.", sender: 'bot' },
        ]);
      }
    }
  };

  return (
    <div className={`chat-app ${darkMode ? 'dark' : ''}`}>
      <div className="sidebar">
        <div className="header">
          <div className="subtitle">Marketing</div>
          <div className="title">ChatBot</div>
        </div>

        <nav className="nav">
          <div className="nav-item" onClick={() => setActiveTab('favorite')}>
            <FiHeart className="nav-icon" /> Favorite
          </div>
          <div className="nav-item" onClick={() => setActiveTab('history')}>
            <FiClock className="nav-icon" /> History
          </div>
          <div className="nav-item" onClick={() => setActiveTab('settings')}>
            <FiSettings className="nav-icon" /> Settings
          </div>
        </nav>

        <div className="auth-section">
          {currentUser ? (
            <div className="user-info">
              <span>Welcome, {currentUser.username}</span>
              <button className="logout-btn" onClick={handleLogout}>
                Logout
              </button>
            </div>
          ) : (
            <button
              className="login-btn"
              onClick={() => {
                setShowAuthModal(true);
                setIsLoginView(true);
              }}
            >
              Login
            </button>
          )}
        </div>
      </div>

      <div className="main-content">
        {activeTab === 'settings' ? (
          <div className="settings-container">
            <h2>
              <FiSettings /> Settings
            </h2>
            <div className="theme-toggle">
              <label>
                {darkMode ? <FiMoon /> : <FiSun />}
                <span>Dark Mode</span>
                <input
                  type="checkbox"
                  checked={darkMode}
                  onChange={() => setDarkMode(!darkMode)}
                />
              </label>
            </div>
          </div>
        ) : (
          <>
            <div className="chat-messages">
              {messages.map((msg, i) => (
                <div key={i} className={`message ${msg.sender}`}>
                  {msg.text}
                </div>
              ))}
            </div>

            {suggestions.length > 0 && (
              <div className="suggestions bg-gray-100 p-2 rounded-md shadow-sm mb-2">
                {suggestions.map((sug, index) => (
                  <div
                    key={index}
                    className="suggestion-item cursor-pointer hover:bg-gray-200 p-1"
                    onClick={() => setInputMessage(sug)}
                  >
                    {sug}
                  </div>
                ))}
              </div>
            )}

            <form className="message-input" onSubmit={handleSendMessage}>
              <input
                type="text"
                placeholder="Ask Anything?"
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
              />
              <button type="submit">
                <FiArrowRight />
              </button>
            </form>
          </>
        )}
      </div>

      {showAuthModal && (
        <div className="auth-modal">
          <div className="auth-box">
            <button
              className="close-btn"
              onClick={() => {
                setShowAuthModal(false);
                setError('');
              }}
            >
              <FiX />
            </button>
            <h2>{isLoginView ? 'Login' : 'Sign Up'}</h2>
            {error && <div className="error-message">{error}</div>}
            <form onSubmit={isLoginView ? handleLogin : handleSignup}>
              {!isLoginView && (
                <input
                  type="text"
                  name="username"
                  placeholder="Username"
                  value={formData.username}
                  onChange={handleInputChange}
                  required
                />
              )}
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleInputChange}
                required
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleInputChange}
                required
              />
              <button type="submit">{isLoginView ? 'Login' : 'Sign Up'}</button>
            </form>
            <div className="auth-switch">
              {isLoginView ? "Don't have an account? " : 'Already have an account? '}
              <span
                onClick={() => {
                  setIsLoginView(!isLoginView);
                  setError('');
                }}
              >
                {isLoginView ? 'Sign Up' : 'Login'}
              </span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ChatApp;
