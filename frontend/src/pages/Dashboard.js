import React, { useState } from 'react';
import '../style/pages/Dashboard.css';
import Navbar from '../components/Navbar';
import Profile from '../components/Profile';
import ProfileSettings from '../components/ProfileSettings';
import MedicalHistory from '../components/MedicalHistory';
// import SavedMedications from '../components/SavedMedications';
import HealthInsights from '../components/HealthInsights';
import PrivacyControls from '../components/PrivacyControls';
import MedicationRecommendation from '../components/MedicationRecommendation';
import DashboardCharts from '../components/DashboardCharts';

const Dashboard = () => {
  const [activeTab, setActiveTab] = useState('profile');

  const renderContent = () => {
    switch (activeTab) {
      case 'profile':
        return <Profile />;
      case 'medicalHistory':
        return <MedicalHistory />;
      case 'medications':
        return <MedicationRecommendation />;
      case 'healthReport':
        return <HealthInsights />;
      case 'charts':
        return <DashboardCharts />;
      case 'settings':
        return <ProfileSettings />;
      case 'privacy':
        return <PrivacyControls />;
      default:
        return <Profile />;
    }
  };

  return (
    <div className="dashboard-container">
      <Navbar />
      <div className="dashboard-sidebar">
        <button
          className={activeTab === 'profile' ? 'active' : ''}
          onClick={() => setActiveTab('profile')}
          aria-label="View Profile Settings"
        >
          Profile
        </button>
        <button
          className={activeTab === 'medicalHistory' ? 'active' : ''}
          onClick={() => setActiveTab('medicalHistory')}
          aria-label="View Medical History"
        >
          Medical History
        </button>
        <button
          className={activeTab === 'medications' ? 'active' : ''}
          onClick={() => setActiveTab('medications')}
          aria-label="View Medication Recommendations"
        >
          Medications
        </button>
        <button
          className={activeTab === 'healthReport' ? 'active' : ''}
          onClick={() => setActiveTab('healthReport')}
          aria-label="View Health Reports"
        >
          Health Report
        </button>
        <button
          className={activeTab === 'charts' ? 'active' : ''}
          onClick={() => setActiveTab('charts')}
          aria-label="View Dashboard Charts"
        >
          Charts
        </button>
        <button
          className={activeTab === 'settings' ? 'active' : ''}
          onClick={() => setActiveTab('settings')}
          aria-label="Edit Profile Settings"
        >
          Settings
        </button>
        <button
          className={activeTab === 'privacy' ? 'active' : ''}
          onClick={() => setActiveTab('privacy')}
          aria-label="Manage Privacy Controls"
        >
          Privacy
        </button>
      </div>
      <div className="dashboard-content">
        <h1>Welcome to Your Dashboard</h1>
        <div className="dashboard-section">{renderContent()}</div>
      </div>
    </div>
  );
};

export default Dashboard;
