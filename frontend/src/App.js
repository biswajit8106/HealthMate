import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Home from './pages/Home';
// import Diagnosis from './pages/Diagnosis';
import SymptomCheckerPage from './pages/SymptomCheckerPage';
import ReportAnalyzer from './components/ReportAnalyzer';
import Dashboard from './pages/Dashboard';
import ReportPage from './pages/ReportPage'; 
import MedicationReminderForm from './components/MedicationReminderForm';
import AdminPanel from './pages/Admin/AdminPanel';
import AdminLogin from './pages/Admin/AdminLogin';
import './style/styles.css';

import { AuthContext } from './context/AuthContext';

function AppRoutes() {
  const { isAuthenticated } = useContext(AuthContext);

  return (
    <Routes>
      <Route path="/" element={<Home />} />
      {/* <Route path="/diagnosis" element={<Diagnosis />} /> */}
      <Route path="/symptom-checker" element={<SymptomCheckerPage />} />
      <Route path="/report" element={<ReportPage />} /> 
      <Route path="/reportanalyzer" element={<ReportAnalyzer />} />
      <Route path="/medication-reminder" element={<MedicationReminderForm />} />
      {/* <Route path="/admin" element={<AdminPanel />} /> */}
      {/* <Route path="/admin/login" element={<AdminLogin />} /> */}
      {/* <Route path="/admin/dashboard" element={<AdminDashboard />} /> */}
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
