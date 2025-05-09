import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import LoginModal from './LoginModal';
import SignupModal from './SignupModal';
import logo from '../assets/logo.png';
import '../style/components/Navbar.css';

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);

  useEffect(() => {
    const token = localStorage.getItem('token');
    setIsLoggedIn(!!token);
  }, []);

  const handleLoginSuccess = () => {
    setIsLoggedIn(true);
  };

  const handleSwitchToSignup = () => {
    setShowLoginModal(false);
    setShowSignupModal(true);
  };

  const handleSwitchToLogin = () => {
    setShowSignupModal(false);
    setShowLoginModal(true);
  };

  const toggleLoginModal = () => {
    setShowLoginModal(!showLoginModal);
    setShowSignupModal(false);
  };

  const toggleSignupModal = () => {
    setShowSignupModal(!showSignupModal);
    setShowLoginModal(false);
  };

  const handleSymptomCheckerClick = () => {
    if (!isLoggedIn) {
      toggleLoginModal();
    } else {
      navigate('/symptom-checker');
    }
  };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <img src={logo} alt="Health-mate logo" className="navbar-logo-img" />
          <span className="navbar-logo-text">HealthMate</span>
        </Link>

        <div className="navbar-links">
          {isLoggedIn && (
            <>
             <button><Link to="/">Home</Link></button>
              <button className="symptom-button" onClick={handleSymptomCheckerClick}>
               Symptom Checker
               </button>
               <button><Link to="/reportanalyzer">Report Analyzer</Link></button>
              <button><Link to="/dashboard">Dashboard</Link></button>
               {/* <Link to="/chat">AI Doctor Chat</Link> */}
            </>
          )}
        </div>

        <div className="navbar-buttons">
          {isLoggedIn ? (
            <button 
              className="navbar-button"
              onClick={() => {
                localStorage.removeItem('token');
                localStorage.removeItem('user');
                setIsLoggedIn(false);
                navigate('/');
              }}
            >
              Logout
            </button>
          ) : (
            <>
              <button className="navbar-button" onClick={toggleLoginModal}>
                Login
              </button>
              <button className="navbar-button" onClick={toggleSignupModal}>
                Sign Up
              </button>
            </>
          )}
        </div>
      </div>

      <LoginModal 
        show={showLoginModal} 
        onClose={toggleLoginModal}
        onSwitchToSignup={handleSwitchToSignup}
        onLoginSuccess={handleLoginSuccess}
      />
      <SignupModal 
        show={showSignupModal} 
        onClose={toggleSignupModal}
        onSwitchToLogin={handleSwitchToLogin}
      />
    </nav>
  );
};

export default Navbar;
