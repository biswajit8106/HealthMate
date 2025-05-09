import React from 'react';
import SymptomChecker from '../components/SymptomChecker';  // Importing the SymptomChecker component
import Navbar from '../components/Navbar';
import '../style/pages/SymptomCheckerPage.css';

const SymptomCheckerPage = () => {
  return (
    <div className="symptom-checker-page">
      <Navbar />
      <div className="symptom-checker-container">
        <SymptomChecker />
      </div>
    </div>
  );
};

export default SymptomCheckerPage;
