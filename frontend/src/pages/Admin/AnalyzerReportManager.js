import React, { useEffect, useState } from 'react';
import axios from 'axios';

import '../../style/pages/AnalyzerReportManager.css';

const AnalyzerReportManager = () => {
  const [uploads, setUploads] = useState([]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(true);

  const fetchUploads = async () => {
    try {
      const res = await axios.get('http://localhost:5000/admin/analyzer_reports/');
      setUploads(res.data);
    } catch (err) {
      setError('Failed to fetch analyzer uploads');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUploads();
  }, []);

  const downloadUpload = (filename) => {
    window.open(`http://localhost:5000/admin/analyzer_reports/download/${filename}`, '_blank');
  };

  const deleteUpload = async (filename) => {
    try {
      await axios.delete(`http://localhost:5000/admin/analyzer_reports/delete/${filename}`);
      fetchUploads();
    } catch (err) {
      setError('Failed to delete upload');
      console.error(err);
    }
  };

  if (loading) return <p>Loading analyzer uploads...</p>;
  if (error) return <p className="error">{error}</p>;

  return (
    <div>
      <h2>Analyzer Report Management</h2>
      <table>
        <thead>
          <tr>
            <th>Filename</th>
            <th>Size (bytes)</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {uploads.map(upload => (
            <tr key={upload.filename}>
              <td>{upload.filename}</td>
              <td>{upload.size}</td>
              <td>
                <button onClick={() => downloadUpload(upload.filename)}>Download</button>
                <button onClick={() => deleteUpload(upload.filename)}>Delete</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default AnalyzerReportManager;
