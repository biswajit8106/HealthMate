import React, { useEffect, useState } from 'react';
import axios from 'axios';

import '../../style/pages/SystemLogsSecurity.css';

const SystemLogsSecurity = () => {
  const [activityLogs, setActivityLogs] = useState([]);
  const [failedLogins, setFailedLogins] = useState([]);
  const [sessions, setSessions] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchLogs = async () => {
    try {
      const [activityRes, failedRes, sessionsRes] = await Promise.all([
        axios.get('http://localhost:5000/admin/system_logs/activity'),
        axios.get('http://localhost:5000/admin/system_logs/failed_logins'),
        axios.get('http://localhost:5000/admin/system_logs/session_management'),
      ]);
      setActivityLogs(activityRes.data);
      setFailedLogins(failedRes.data);
      setSessions(sessionsRes.data);
    } catch (err) {
      setError('Failed to fetch system logs');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLogs();
  }, []);

  if (loading) return <p>Loading system logs...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h2>System Logs & Security</h2>
      <h3>Activity Logs</h3>
      <ul>
        {activityLogs.map((log, index) => (
          <li key={index}>{JSON.stringify(log)}</li>
        ))}
      </ul>
      <h3>Failed Login Attempts</h3>
      <ul>
        {failedLogins.map((fail, index) => (
          <li key={index}>{JSON.stringify(fail)}</li>
        ))}
      </ul>
      <h3>Sessions</h3>
      <ul>
        {sessions.map((session) => (
          <li key={session.session_id}>
            Session ID: {session.session_id}, Admin ID: {session.admin_id}, Login Time: {session.login_time}, Active: {session.active ? 'Yes' : 'No'}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default SystemLogsSecurity;
