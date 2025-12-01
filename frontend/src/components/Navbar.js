import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
// import { useTranslation } from 'react-i18next';
import LoginModal from './LoginModal';
import SignupModal from './SignupModal';
import logo from '../assets/logo.png';
import '../style/components/Navbar.css';

const Navbar = () => {
  // const { t, i18n } = useTranslation();
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);


  useEffect(() => {
    // Check session from backend instead of localStorage token
    const checkSession = async () => {
      try {
        const response = await fetch('https://healthmate-y0dn.onrender.com/api/user/session', {
          credentials: 'include',
        });
        const data = await response.json();
        setIsLoggedIn(data.logged_in === true);
      } catch (error) {
        setIsLoggedIn(false);
      }
    };
    checkSession();
  }, []);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (isMobileMenuOpen && !event.target.closest('.navbar-container')) {
        setIsMobileMenuOpen(false);
      }
    };

    if (isMobileMenuOpen) {
      document.addEventListener('click', handleClickOutside);
    }

    return () => {
      document.removeEventListener('click', handleClickOutside);
    };
  }, [isMobileMenuOpen]);

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
    setIsMobileMenuOpen(false);
  };
  const handleReportAnalyzerClick = () => {
    if (!isLoggedIn) {
      toggleLoginModal();
    } else {
      navigate('/reportanalyzer');
    }
    setIsMobileMenuOpen(false);
  };

  const handleMedicationReminderClick = () => {
    if (!isLoggedIn) {
      toggleLoginModal();
    } else {
      navigate('/medication-reminder');
    }
    setIsMobileMenuOpen(false);
  };
  const handleDashboardClick = () => {
    if (!isLoggedIn) {
      toggleLoginModal();
    } else {
      navigate('/dashboard');
    }
    setIsMobileMenuOpen(false); // Close menu after navigation
  };

  const handleLinkClick = () => {
    setIsMobileMenuOpen(false); // Close menu after navigation
  };

  // const changeLanguage = (lng) => {
  //   i18n.changeLanguage(lng);
  //   setLanguage(lng);
  // };

  return (
    <nav className="navbar">
      <div className="navbar-container">
        <Link to="/" className="navbar-logo">
          <img src={logo} alt="Health-mate logo" className="navbar-logo-img" />
          <span className="navbar-logo-text">HealthMate</span>
        </Link>

        <div className={`navbar-links ${isMobileMenuOpen ? 'active' : ''}`}>
          {isLoggedIn && (
            <>
             <button onClick={() => { navigate('/'); setIsMobileMenuOpen(false); }}>Home</button>
              <button className="symptom-button" onClick={handleSymptomCheckerClick}>
               Symptom Diagnosis
               </button>
               <button className="reportanalyzer-button" onClick={handleReportAnalyzerClick}>
               Report Analyzer</button>
                <button className="medication-button" onClick={handleMedicationReminderClick}>
                Medication Reminder</button>
                <button className="dashboard-button" onClick={handleDashboardClick}>
                Dashboard</button>
            </>
          )}
          <div className="auth-buttons-mobile">
            {isLoggedIn ? (
              <button
                className="navbar-button"
                onClick={async () => {
                  try {
                    await fetch('https://healthmate-y0dn.onrender.com/api/user/logout', {
                      method: 'POST',
                      credentials: 'include',
                    });
                  } catch (error) {
                    console.error('Logout failed', error);
                  }
                  setIsLoggedIn(false);
                  navigate('/');
                  setIsMobileMenuOpen(false);
                }}
              >
                Logout
              </button>
            ) : (
              <>
                <button className="navbar-button" onClick={() => { toggleLoginModal(); setIsMobileMenuOpen(false); }}>
                  Login
                </button>
                <button className="navbar-button" onClick={() => { toggleSignupModal(); setIsMobileMenuOpen(false); }}>
                  Sign Up
                </button>
              </>
            )}
          </div>
        </div>

        {/* <div className="language-selector">
          <select value={language} onChange={(e) => changeLanguage(e.target.value)}>
            <option value="en">English</option>
            <option value="hi">हिन्दी</option>
          </select>
        </div> */}

        <div className="navbar-buttons">
          {isLoggedIn ? (
            <button
              className="navbar-button"
              onClick={async () => {
                try {
                  await fetch('https://healthmate-y0dn.onrender.com/api/user/logout', {
                    method: 'POST',
                    credentials: 'include',
                  });
                } catch (error) {
                  console.error('Logout failed', error);
                }
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

        <button className="hamburger" onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}>
          <span className="bar"></span>
          <span className="bar"></span>
          <span className="bar"></span>
        </button>
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
