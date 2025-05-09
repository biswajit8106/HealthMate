import React, { useEffect, useState } from 'react';
import axios from 'axios';

import '../../style/pages/Settings.css';

const Settings = () => {
  const [settings, setSettings] = useState({
    max_file_size: 10485760,
    report_retention_days: 365,
    ml_confidence_threshold: 0.8,
  });
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchSettings = async () => {
    try {
      const res = await axios.get('http://localhost:5000/admin/settings/');
      setSettings(res.data);
    } catch (err) {
      setError('Failed to fetch settings');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSettings();
  }, []);

  const updateSettings = async () => {
    try {
      await axios.put('http://localhost:5000/admin/settings/', settings);
      alert('Settings updated successfully');
    } catch (err) {
      setError('Failed to update settings');
      console.error(err);
    }
  };

  if (loading) return <p>Loading settings...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h2>Settings</h2>
      <div>
        <label>
          Max File Size (bytes):
          <input
            type="number"
            value={settings.max_file_size}
            onChange={(e) => setSettings({ ...settings, max_file_size: Number(e.target.value) })}
          />
        </label>
      </div>
      <div>
        <label>
          Report Retention (days):
          <input
            type="number"
            value={settings.report_retention_days}
            onChange={(e) => setSettings({ ...settings, report_retention_days: Number(e.target.value) })}
          />
        </label>
      </div>
      <div>
        <label>
          ML Model Confidence Threshold:
          <input
            type="number"
            step="0.01"
            min="0"
            max="1"
            value={settings.ml_confidence_threshold}
            onChange={(e) => setSettings({ ...settings, ml_confidence_threshold: parseFloat(e.target.value) })}
          />
        </label>
      </div>
      <button onClick={updateSettings}>Update Settings</button>
    </div>
  );
};

export default Settings;
