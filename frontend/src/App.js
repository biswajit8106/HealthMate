import React, { useContext, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate, useNavigate } from 'react-router-dom';
import Home from './pages/Home';
// import Diagnosis from './pages/Diagnosis';
import SymptomCheckerPage from './pages/SymptomCheckerPage';
import ReportAnalyzer from './components/ReportAnalyzer';
import Dashboard from './pages/Dashboard';
import ReportPage from './pages/ReportPage'; 
// import MedicationReminder from './components/MedicationReminder';
import AdminPanel from './pages/Admin/AdminPanel';
import AdminLogin from './pages/Admin/AdminLogin';
import AdminDashboard from './pages/Admin/AdminDashboard';
import './style/styles.css';

import { AuthContext } from './context/AuthContext';
import MedicationReminder from './components/MedicationReminder';
import { requestNotificationPermissionAndSendToken, listenForForegroundMessages } from './utils/notificationService';

function MedicationReminderWrapper() {
  const navigate = useNavigate();

  const handleSave = (reminderData) => {
    console.log('Saving reminder data:', reminderData);
    // TODO: Add actual save logic here, e.g., API call to backend
    navigate('/dashboard'); // Navigate away after save
  };

  const handleClose = () => {
    navigate('/dashboard'); // Navigate away on close
  };

  return <MedicationReminder onSave={handleSave} onClose={handleClose} />;
}

function AppRoutes() {
  const { isAuthenticated, user } = React.useContext(AuthContext);

  React.useEffect(() => {
    if (user && user.id) {
      requestNotificationPermissionAndSendToken(user.id);
      listenForForegroundMessages((payload) => {
        // You can customize notification display here
        console.log('Foreground notification:', payload);
      });
    }
  }, [user]);

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      {/* <Route path="/diagnosis" element={<Diagnosis />} /> */}
      <Route path="/symptom-checker" element={<SymptomCheckerPage />} />
      <Route path="/report" element={<ReportPage />} /> 
      <Route path="/reportanalyzer" element={<ReportAnalyzer />} />
      <Route path="/medication-reminder" element={<MedicationReminderWrapper />} />
      <Route path="/admin" element={<AdminPanel />} />
      <Route path="/admin/login" element={<AdminLogin />} /> 
      <Route path="/admin/dashboard" element={<AdminDashboard />} /> 
      <Route 
        path="/dashboard" 
        element={
          isAuthenticated ? (
            <Dashboard />
          ) : (
            <Navigate to="/dashboard" />
          )
        } 
      />
      <Route
        path="/admin"
        element={
          isAuthenticated ? (
            <AdminPanel />
          ) : (
            <Navigate to="/admin/login" />
          )
        }
      />
      <Route path="/admin/login" element={<AdminLogin />} />
    </Routes>
  );
}

function App() {
  return (
    <Router>
      <div className="App">
        <AppRoutes />
      </div>
    </Router>
  );
}

export default App;
