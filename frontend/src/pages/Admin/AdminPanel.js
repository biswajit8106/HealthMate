import React, { useState } from 'react';

import UserManagement from './UserManagement';
import HealthReportsManager from './HealthReportsManager';
import AnalyzerReportManager from './AnalyzerReportManager';
import AdminDashboard from './AdminDashboard';
import DiseaseInformationManager from './DiseaseInformationManager';
import AdminUserControls from './AdminUserControls';
import SystemLogsSecurity from './SystemLogsSecurity';
import FeedbackContactRequests from './FeedbackContactRequests';
import Settings from './Settings';

import '../../style/pages/AdminPanel.css';

const AdminPanel = () => {
  const [activeTab, setActiveTab] = useState('dashboard');

  const renderContent = () => {
    switch (activeTab) {
      case 'dashboard':
        return <AdminDashboard />;
      case 'userManagement':
        return <UserManagement />;
      case 'healthReports':
        return <HealthReportsManager />;
      case 'analyzerReports':
        return <AnalyzerReportManager />;
      case 'diseaseInformation':
        return <DiseaseInformationManager />;
      case 'adminUserControls':
        return <AdminUserControls />;
      case 'systemLogsSecurity':
        return <SystemLogsSecurity />;
      case 'feedbackContactRequests':
        return <FeedbackContactRequests />;
      case 'settings':
        return <Settings />;
      default:
        return <AdminDashboard />;
    }
  };

  return (
    <div className="admin-panel-container">
      <div className="admin-sidebar">
        <button onClick={() => setActiveTab('dashboard')}>Dashboard</button>
        <button onClick={() => setActiveTab('userManagement')}>User Management</button>
        <button onClick={() => setActiveTab('healthReports')}>Health Reports</button>
        <button onClick={() => setActiveTab('analyzerReports')}>Analyzer Reports</button>
        <button onClick={() => setActiveTab('diseaseInformation')}>Disease Information</button>
        <button onClick={() => setActiveTab('adminUserControls')}>Admin User Controls</button>
        <button onClick={() => setActiveTab('systemLogsSecurity')}>System Logs & Security</button>
        <button onClick={() => setActiveTab('feedbackContactRequests')}>Feedback & Contact Requests</button>
        <button onClick={() => setActiveTab('settings')}>Settings</button>
      </div>
      <div className="admin-content">
        {renderContent()}
      </div>
    </div>
  );
};

export default AdminPanel;
