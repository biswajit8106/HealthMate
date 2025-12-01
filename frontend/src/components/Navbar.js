import React, { useState, useEffect, useRef } from "react";
import { Link, useNavigate } from "react-router-dom";
import LoginModal from "./LoginModal";
import SignupModal from "./SignupModal";
import logo from "../assets/logo.png";
import "../style/components/Navbar.css";

const Navbar = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const navigate = useNavigate();
  const [showLoginModal, setShowLoginModal] = useState(false);
  const [showSignupModal, setShowSignupModal] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  const menuRef = useRef(null);
  const buttonRef = useRef(null);

  // Check Session
  useEffect(() => {
    const checkSession = async () => {
      try {
        const res = await fetch(
          "https://healthmate-y0dn.onrender.com/api/user/session",
          { credentials: "include" }
        );
        const data = await res.json();
        setIsLoggedIn(data.logged_in === true);
      } catch {
        setIsLoggedIn(false);
      }
    };
    checkSession();
  }, []);

  // Close menu on outside click
  useEffect(() => {
    const handleClose = (e) => {
      if (
        isMobileMenuOpen &&
        menuRef.current &&
        !menuRef.current.contains(e.target) &&
        !buttonRef.current.contains(e.target)
      ) {
        setIsMobileMenuOpen(false);
      }
    };

    document.addEventListener("mousedown", handleClose);
    return () => document.removeEventListener("mousedown", handleClose);
  }, [isMobileMenuOpen]);

  const closeAndGo = (path) => {
    navigate(path);
    setIsMobileMenuOpen(false);
  };

  return (
    <>
      <nav className="navbar">
        <div className="navbar-container">
          {/* Logo */}
          <Link to="/" className="navbar-logo" onClick={() => closeAndGo("/")}>
            <img src={logo} alt="HealthMate Logo" className="navbar-logo-img" />
            <span className="navbar-logo-text">HealthMate</span>
          </Link>

          {/* Desktop Links */}
          <div className="navbar-links-desktop">
            {isLoggedIn && (
              <>
                <button onClick={() => navigate("/")}>Home</button>
                <button onClick={() => navigate("/symptom-checker")}>
                  Symptom Diagnosis
                </button>
                <button onClick={() => navigate("/reportanalyzer")}>
                  Report Analyzer
                </button>
                <button onClick={() => navigate("/medication-reminder")}>
                  Medication Reminder
                </button>
                <button onClick={() => navigate("/dashboard")}>Dashboard</button>
              </>
            )}
          </div>

          {/* Desktop Auth */}
          <div className="auth-desktop">
            {isLoggedIn ? (
              <button
                className="navbar-button"
                onClick={async () => {
                  await fetch(
                    "https://healthmate-y0dn.onrender.com/api/user/logout",
                    { method: "POST", credentials: "include" }
                  );
                  setIsLoggedIn(false);
                }}
              >
                Logout
              </button>
            ) : (
              <>
                <button className="navbar-button" onClick={() => setShowLoginModal(true)}>
                  Login
                </button>
                <button className="navbar-button" onClick={() => setShowSignupModal(true)}>
                  Sign Up
                </button>
              </>
            )}
          </div>

          {/* Hamburger */}
          <button
            className={`hamburger ${isMobileMenuOpen ? "active" : ""}`}
            ref={buttonRef}
            onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          >
            <span className="bar"></span>
            <span className="bar"></span>
            <span className="bar"></span>
          </button>
        </div>
      </nav>

      {/* Overlay */}
      {isMobileMenuOpen && <div className="menu-overlay"></div>}

      {/* Sliding Mobile Menu */}
      <div
        ref={menuRef}
        className={`mobile-menu ${isMobileMenuOpen ? "open" : ""}`}
      >
        {isLoggedIn ? (
          <>
            <button onClick={() => closeAndGo("/")}>Home</button>
            <button onClick={() => closeAndGo("/symptom-checker")}>
              Symptom Diagnosis
            </button>
            <button onClick={() => closeAndGo("/reportanalyzer")}>
              Report Analyzer
            </button>
            <button onClick={() => closeAndGo("/medication-reminder")}>
              Medication Reminder
            </button>
            <button onClick={() => closeAndGo("/dashboard")}>Dashboard</button>
            <button
              className="navbar-button"
              onClick={async () => {
                await fetch(
                  "https://healthmate-y0dn.onrender.com/api/user/logout",
                  { method: "POST", credentials: "include" }
                );
                setIsLoggedIn(false);
                closeAndGo("/");
              }}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <button className="navbar-button" onClick={() => { setShowLoginModal(true); setIsMobileMenuOpen(false); }}>Login</button>
            <button className="navbar-button" onClick={() => { setShowSignupModal(true); setIsMobileMenuOpen(false); }}>Sign Up</button>
          </>
        )}
      </div>

      <LoginModal show={showLoginModal} onClose={() => setShowLoginModal(false)} />
      <SignupModal show={showSignupModal} onClose={() => setShowSignupModal(false)} />
    </>
  );
};

export default Navbar;
