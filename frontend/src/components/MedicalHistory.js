import React, { useEffect, useState } from 'react';
import axios from 'axios';

const MedicalHistory = () => {
  const [reports, setReports] = useState([]);
  const [selectedReport, setSelectedReport] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/user/medical_history', {
          withCredentials: true,
        });
        setReports(response.data);
        if (response.data.length > 0) {
          setSelectedReport(response.data[0]);
        } else {
          setSelectedReport(null);
        }
      } catch (error) {
        console.error('Failed to fetch medical history', error);
        setError('Failed to fetch medical history');
      }
    };
    fetchHistory();
  }, []);

  const handleSelectReport = (report) => {
    setSelectedReport(report);
  };

  return (
    <div className="widget medical-history">
      <h2>Medical History</h2>
      {error && <p>{error}</p>}
      {!reports.length ? (
        <p>No medical history reports found.</p>
      ) : (
        <div style={{ display: 'flex' }}>
          <ul style={{ width: '30%', listStyleType: 'none', padding: 0 }}>
            {reports.map((report) => (
              <li
                key={report.id}
                onClick={() => handleSelectReport(report)}
                style={{
                  cursor: 'pointer',
                  padding: '8px',
                  backgroundColor: selectedReport && selectedReport.id === report.id ? '#ddd' : 'transparent',
                }}
              >
                {report.name} - {new Date(report.created_at).toLocaleDateString()}
              </li>
            ))}
          </ul>
          <div style={{ marginLeft: '20px', width: '70%' }}>
            {selectedReport ? (
              <div>
                <p><strong>Disease:</strong> {selectedReport.predicted_disease}</p>
                <p><strong>Date:</strong> {new Date(selectedReport.created_at).toLocaleDateString()}</p>
                <p><strong>Confidence:</strong> {selectedReport.confidence}</p>
                <p><strong>Description:</strong> {selectedReport.description}</p>
                <p><strong>Precautions:</strong> {selectedReport.precautions.join(', ')}</p>
                <p><strong>Medications:</strong> {selectedReport.medications.join(', ')}</p>
                <p><strong>Diets:</strong> {selectedReport.diets.join(', ')}</p>
                <p><strong>Workouts:</strong> {selectedReport.workouts.join(', ')}</p>
              </div>
            ) : (
              <p>Select a report to see details</p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default MedicalHistory;
