import React, { useState } from 'react';
import axios from 'axios';
import '../style/components/SignupModal.css';

const SignupModal = ({ show, onClose, onSwitchToLogin }) => {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    age: '',
    gender: '', // New field for gender
    password: ''
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await axios.post('http://localhost:5000/register', formData);
      if (response.data.message) {
        setError(response.data.message);
      }

      if (response.data.success) {
        // Handle successful signup
        onClose();
        // Optionally redirect or show success message
      } else {
        setError(response.data.message || 'Signup failed');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred during signup');
      // Additional handling for duplicate email error
      if (err.response?.data?.message === 'User already registered.') {
        setError('This email is already registered. Please use a different email.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={`signup-modal ${show ? 'show' : ''}`}>
      <div className="signup-modal-content">
        <h2>Sign Up</h2>
        {error && <div className="error-message">{error}</div>}
        
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              name="username"
              placeholder="Username"
              value={formData.username}
              onChange={handleChange}
              required
              className="signup-input"
            />
          </div>
          
          <div className="form-group">
            <input
              type="email"
              name="email"
              placeholder="Email"
              value={formData.email}
              onChange={handleChange}
              required
              className="signup-input"
            />
          </div>
           
          <div className="form-group">
            <input
              type="integer"
              name="age"
              placeholder="Age"
              value={formData.age}
              onChange={handleChange}
              required
              className="signup-input"
            />
          </div>

          <div className="form-group">
              <label>Gender:</label>
              <div>
                  <label>
                      <input
                          type="radio"
                          name="gender"
                          value="Male"
                          checked={formData.gender === 'Male'}
                          onChange={handleChange}
                          required
                      />
                      Male
                  </label>
                  <label>
                      <input
                          type="radio"
                          name="gender"
                          value="Female"
                          checked={formData.gender === 'Female'}
                          onChange={handleChange}
                          required
                      />
                      Female
                  </label>
                  <label>
                      <input
                          type="radio"
                          name="gender"
                          value="Other"
                          checked={formData.gender === 'Other'}
                          onChange={handleChange}
                          required
                      />
                      Other
                  </label>
              </div>
          </div>
          
          <div className="form-group">
            <input
              type="password"
              name="password"
              placeholder="Password"
              value={formData.password}
              onChange={handleChange}
              required
              className="signup-input"
            />
          </div>
          
          <button 
            type="submit" 
            className="signup-submit-btn"
            disabled={loading}
          >
            {loading ? 'Signing Up...' : 'Sign Up'}
          </button>
        </form>

        <div className="login-alternate-action">
          Already have an account?{' '}
          <a 
            href="#login" 
            onClick={(e) => {
              e.preventDefault();
              onSwitchToLogin();
            }}
          >
            Login
          </a>
        </div>
        
        <button 
          className="close-modal" 
          onClick={onClose}
          disabled={loading}
        >
          Close
        </button>
      </div>
    </div>
  );
};

export default SignupModal;
