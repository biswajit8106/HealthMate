import React from 'react';
import '../style/components/ForgotPasswordModal.css';

const ForgotPasswordModal = ({ show, onClose }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    // Handle forgot password submission
    onClose();
  };

  return (
    <div className={`forgot-password-modal ${show ? 'show' : ''}`}>
      <div className="forgot-password-modal-content">
        <h2>Reset Password</h2>
        <form onSubmit={handleSubmit}>
          <input 
            type="email" 
            placeholder="Enter your email" 
            required 
          />
          <button type="submit">Send Reset Link</button>
        </form>
        <button className="close-modal" onClick={onClose}>Close</button>
      </div>
    </div>
  );
};

export default ForgotPasswordModal;
