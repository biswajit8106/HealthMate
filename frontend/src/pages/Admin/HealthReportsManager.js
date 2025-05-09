import React, { useEffect, useState } from 'react';
import axios from 'axios';

import '../../style/pages/HealthReportsManager.css';

const HealthReportsManager = () => {
  const [reports, setReports] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchReports = async () => {
    try {
      const res = await axios.get('http://localhost:5000/admin/health_reports/');
      setReports(res.data);
    } catch (err) {
      setError('Failed to fetch health reports');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchReports();
  }, []);

  const downloadReport = (id) => {
    window.open(`http://localhost:5000/admin/health_reports/download/${id}`, '_blank');
  };

  const deleteReport = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/admin/health_reports/delete/${id}`);
      fetchReports();
    } catch (err) {
      setError('Failed to delete report');
      console.error(err);
    }
  };

  if (loading) return <p>Loading health reports...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h2>Health Reports Manager</h2>
      <table>
        <thead>
          <tr>
            <th>Report ID</th>
            <th>User ID</th>
            <th>Name</th>
            <th>Predicted Disease</th>
            <th>Confidence</th>
            <th>Created At</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {reports.map(report => (
            <tr key={report.id}>
              <td>{report.id}</td>
              <td>{report.user_id}</td>
              <td>{report.name}</td>
              <td>{report.predicted_disease}</td>
              <td>{report.confidence.toFixed(2)}</td>
              <td>{new Date(report.created_at).toLocaleString()}</td>
              <td>
                <button onClick={() => downloadReport(report.id)}>Download</button>
                <button onClick={() => deleteReport(report.id)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default HealthReportsManager;
