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

  // Password validation function
  const validatePassword = (password) => {
    // Password must be at least 8 characters, contain uppercase, lowercase, digit, and special character
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$/;
    return passwordRegex.test(password);
  };

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null);

    // Validate age before submitting
    const ageNum = Number(formData.age);
    if (!Number.isInteger(ageNum) || ageNum <= 1 || ageNum > 100) {
      setError('Please enter a valid age between 1 and 100.');
      return;
    }

    // Validate password before submitting
    if (!validatePassword(formData.password)) {
      setError('Password must be at least 8 characters long and include uppercase, lowercase, digit, and special character.');
      return;
    }

    setLoading(true);

    try {
      const response = await axios.post('https://healthmate-y0dn.onrender.com/api/user/register', formData);
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
              type="number"
              name="age"
              placeholder="Age"
              value={formData.age}
              onChange={handleChange}
              required
              className="signup-input"
              min="1"
              max="120"
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
