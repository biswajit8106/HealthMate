import React, { useState, useEffect } from 'react';
import axios from 'axios';

const PrivacyControls = () => {
  const [dataSharing, setDataSharing] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    const fetchPrivacySettings = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:3000/user/privacy', {
          headers: { Authorization: `Bearer ${token}` },
        });
        setDataSharing(response.data.dataSharing);
      } catch (error) {
        console.error('Failed to fetch privacy settings', error);
      }
    };
    fetchPrivacySettings();
  }, []);

  const handleToggle = async () => {
    try {
      const token = localStorage.getItem('token');
      await axios.put(
        'http://localhost:3000/user/privacy',
        { dataSharing: !dataSharing },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setDataSharing(!dataSharing);
      setMessage('Privacy settings updated.');
    } catch (error) {
      setMessage('Failed to update privacy settings.');
      console.error(error);
    }
  };

  const handleDeleteHistory = async () => {
    if (!window.confirm('Are you sure you want to delete your history? This action cannot be undone.')) {
      return;
    }
    try {
      const token = localStorage.getItem('token');
      await axios.delete('http://localhost:3000/user/history', {
        headers: { Authorization: `Bearer ${token}` },
      });
      setMessage('History deleted successfully.');
    } catch (error) {
      setMessage('Failed to delete history.');
      console.error(error);
    }
  };

  return (
    <div className="privacy-controls">
      <h2>Privacy Controls</h2>
      {message && <p className="message">{message}</p>}
      <div>
        <label>
          <input type="checkbox" checked={dataSharing} onChange={handleToggle} />
          Allow data sharing for research and improvements.
        </label>
      </div>
      <button
        onClick={handleDeleteHistory}
        style={{
          marginTop: '1rem',
          backgroundColor: '#e74c3c',
          color: 'white',
          border: 'none',
          padding: '0.5rem 1rem',
          borderRadius: '4px',
          cursor: 'pointer',
        }}
      >
        Delete History
      </button>
    </div>
  );
};

export default PrivacyControls;
