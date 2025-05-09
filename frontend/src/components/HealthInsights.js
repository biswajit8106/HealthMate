import React, { useEffect, useState } from 'react';
import axios from 'axios';

const HealthInsights = () => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchReports = async () => {
      try {
        const token = localStorage.getItem('token');
        const response = await axios.get('http://localhost:5000/report/health/reports', {
          headers: { Authorization: `Bearer ${token}` },
        });
        // Deduplicate reports by predicted_disease and date
        const uniqueReportsMap = {};
        response.data.forEach((report) => {
          const key = report.predicted_disease + report.date;
          if (!uniqueReportsMap[key]) {
            uniqueReportsMap[key] = report;
          }
        });
        const uniqueReports = Object.values(uniqueReportsMap);
        setReports(uniqueReports);
      } catch (err) {
        setError('Failed to fetch health reports.');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };
    fetchReports();
  }, []);

  const downloadReport = async (reportId, reportName) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:5000/report/download/${reportId}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `${reportName}_health_report.pdf`);
      document.body.appendChild(link);
      link.click();
      link.parentNode.removeChild(link);
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to download the report.');
      console.error(err);
    }
  };

  const viewReport = async (reportId) => {
    try {
      const token = localStorage.getItem('token');
      const response = await axios.get(`http://localhost:5000/report/download/${reportId}`, {
        headers: { Authorization: `Bearer ${token}` },
        responseType: 'blob',
      });
      const url = window.URL.createObjectURL(new Blob([response.data], { type: 'application/pdf' }));
      window.open(url, '_blank');
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setError('Failed to view the report.');
      console.error(err);
    }
  };

  if (loading) return <p>Loading health reports...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div className="health-insights">
      <h2>Health Reports</h2>
      {reports.length === 0 ? (
        <p>No health reports found.</p>
      ) : (
        <ul>
          {reports.map((report) => (
            <li key={report.id}>
              <strong>{report.title}</strong> - {new Date(report.date).toLocaleDateString()}
              {' '}
              <button onClick={() => viewReport(report.id)}>View</button>
              {' '}
              <button onClick={() => downloadReport(report.id, report.name)}>Download</button>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default HealthInsights;
