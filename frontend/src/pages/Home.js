import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import Testimonials from '../components/Testimonials';
import Navbar from '../components/Navbar';
import LoginModal from '../components/LoginModal';
import '../style/pages/Home.css';
import doc1img from '../assets/Doc1.jpeg';
import img4 from '../assets/img4.jpg';

const Home = () => {
  const navigate = useNavigate();
  const [showLoginModal, setShowLoginModal] = useState(false);

  // Check if user is authenticated
  const isAuthenticated = () => {
    return localStorage.getItem('token') !== null;
  };

  // Handle "Check Symptoms" Click
  const handleSymptomCheckClick = () => {
    if (isAuthenticated()) {
      navigate('/symptom-checker');
    } else {
      setShowLoginModal(true); // Open login modal if not logged in
    }
  };

  // Handle "Report Analyzer" Click
  const handleReportAnalyzerClick = () => {
    if (isAuthenticated()) {
      navigate('/reportanalyzer');
    } else {
      setShowLoginModal(true); // Open login modal if not logged in
    }
  };

  return (
    <div className="home-page">
      <Navbar />

      {/* Hero Section */}
      <section className="hero-section">
        <div className="hero-content">
          <div className="hero-text">
            <h1>Your Personal Health Assistant</h1>
            <p className="hero-subtext">
              Smart comprehensive healthcare at your fingertips. Instant symptom analysis and personalized health recommendations
            </p>
            <div className="cta-buttons">
              <button className="primary-cta" onClick={handleSymptomCheckClick}>
                <span>Check Symptoms</span>
                <i className="fas fa-arrow-right"></i>
              </button>
            </div>
          </div>
          <div className="hero-img">
            <img src={doc1img} alt="Hero section" />
          </div>
        </div>
      </section>

      {/* Main Features Section */}
      <section className="main-features">
        <h2>OUR SPECIALITIES</h2>
        <div className="features-grid">
          <div className="feature-card">
            <div className="feature-icon">1</div>
            <h3>Symptom Diagnosis</h3>
            <p>Get instant health insights by describing your symptoms</p>
            <button className="feature-link" onClick={handleSymptomCheckClick}>
              Try Now →
            </button>
          </div>
          <div className="feature-card">
            <div className="feature-icon">2</div>
            <h3>Report Analyzer</h3>
            <p>Effective medical health report analyzer.</p>
            <button className="feature-link" onClick={handleReportAnalyzerClick}>
              Go For It →
            </button>
          </div>
          <div className="feature-card">
            <div className="feature-icon">3</div>
            <h3>Medication Reminder</h3>
            <p>Never miss a dose with our smart reminder system</p>
            <Link to="/medication-reminder" className="feature-link">
            Assecible Soon →
            </Link>
          </div>
        </div>
      </section>

      {/* Testimonials Section */}
      <Testimonials />

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-content">
          <div className="footer-image">
            <img src={img4} alt="Footer logo" />
          </div>
          <div className="footer-info">
            <div className="footer-social">
              <a href="https://facebook.com" target="_blank" rel="noopener noreferrer">Facebook</a>
              <a href="https://twitter.com" target="_blank" rel="noopener noreferrer">Twitter</a>
              <a href="https://linkedin.com" target="_blank" rel="noopener noreferrer">LinkedIn</a>
            </div>
            <div className="footer-links">
              <a href="/privacy">Privacy Policy</a>
              <a href="/terms">Terms of Service</a>
              <a href="/contact">Contact Us</a>
            </div>
            <div className="footer-disclaimer">
              <p>Disclaimer: This is an AI tool and does not replace professional medical advice.</p>
            </div>
          </div>
        </div>
      </footer>

      {/* Login Modal - Conditional rendering */}
      {showLoginModal && (
        <LoginModal
          show={showLoginModal}
          onClose={() => setShowLoginModal(false)}
          onSwitchToSignup={() => console.log("Switch to Signup")}
          onLoginSuccess={() => {
            setShowLoginModal(false);
            navigate('/symptom-checker');
          }}
        />
      )}

    </div>
  );
};

export default Home;
