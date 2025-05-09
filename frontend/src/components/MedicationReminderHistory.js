import React, { useEffect, useState } from 'react';
import axios from 'axios';
// import './MedicationReminderHistory.css';

const MedicationReminderHistory = () => {
  const [history, setHistory] = useState([]);
  const [error, setError] = useState('');

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await axios.get('http://localhost:5000/api/medicinereminder/reminder/history', {
          withCredentials: true,
        });
        setHistory(response.data);
      } catch (err) {
        setError('Failed to fetch reminder history: ' + (err.response?.data?.error || err.message));
      }
    };
    fetchHistory();
  }, []);

  return (
    <div className="medication-reminder-history">
      <h2>Medicine Reminder History</h2>
      {error && <p className="error-message">{error}</p>}
      {!history.length ? (
        <p>No reminder history found.</p>
      ) : (
        <table>
          <thead>
            <tr>
              <th>Medicine Name</th>
              <th>Dosage</th>
              <th>Timing</th>
              <th>Frequency</th>
              <th>Notes</th>
              <th>Start Date</th>
              <th>End Date</th>
            </tr>
          </thead>
          <tbody>
            {history.map((item) => (
              <tr key={item.id}>
                <td>{item.medicine_name}</td>
                <td>{item.dosage || '-'}</td>
                <td>{item.timing || '-'}</td>
                <td>{item.frequency || '-'}</td>
                <td>{item.notes || '-'}</td>
                <td>{item.start_date}</td>
                <td>{item.end_date || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default MedicationReminderHistory;
