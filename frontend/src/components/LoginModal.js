import React, { useState } from 'react';
import axios from 'axios';
// Removed unused useNavigate import
import '../style/components/LoginModal.css';

const LoginModal = ({ show, onClose, onSwitchToSignup, onLoginSuccess }) => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null); // Added error state
  // const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', { email, password });
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('user', JSON.stringify(response.data.user));
      // Redirect to home page after successful login
      // navigate('/dashboard');

      onClose(); // Close the modal after successful login
      if (typeof onLoginSuccess === 'function') {
        onLoginSuccess();
      }
    } catch (error) {
      console.error('Login failed:', error);
      setError('Login failed. Please check your credentials.'); // Set error message
    }
  };

  return (
    <div className={`login-modal ${show ? 'show' : ''}`}>
      <div className="login-modal-content">
        <span className="close" onClick={onClose}>&times;</span>
        <h2>Login</h2>
        <form onSubmit={handleSubmit}>
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            className="login-input" // Added class for consistent styling
            autoComplete="email" // Added autocomplete attribute
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            className="login-input" // Added class for consistent styling
            autoComplete="current-password" // Added autocomplete attribute
          />

          <button type="submit" className="login-submit-btn">Login</button>
        </form>
        {error && <div className="error-message">{error}</div>} 
        <button onClick={onSwitchToSignup}>Don't have an account? Sign Up</button>
      </div>
    </div>
  );
};

export default LoginModal;
