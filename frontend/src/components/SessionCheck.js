import React, { useEffect, useState } from 'react';
import axios from 'axios';

const SessionCheck = () => {
  const [sessionInfo, setSessionInfo] = useState(null);
  const [error, setError] = useState(null);

  const checkSession = async () => {
    try {
      const response = await axios.get('http://localhost:5000/session', { withCredentials: true });
      setSessionInfo(response.data);
    } catch (err) {
      setError(err.message || 'Error checking session');
    }
  };

  useEffect(() => {
    checkSession();
  }, []);

  if (error) {
    return <div>Error: {error}</div>;
  }

  if (!sessionInfo) {
    return <div>Loading session info...</div>;
  }

  return (
    <div>
      <h3>Session Info</h3>
      <pre>{JSON.stringify(sessionInfo, null, 2)}</pre>
    </div>
  );
};

export default SessionCheck;
