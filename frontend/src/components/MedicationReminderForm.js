import React, { useState } from 'react';
import axios from 'axios';
import MedicationReminderHistory from './MedicationReminderHistory';

const MedicationReminderForm = () => {
  const [medicineName, setMedicineName] = useState('');
  const [dosage, setDosage] = useState('');
  const [timing, setTiming] = useState('');
  const [frequency, setFrequency] = useState('');
  const [notes, setNotes] = useState('');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [refreshHistory, setRefreshHistory] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');

    if (!medicineName || !startDate) {
      setError('Medicine name and start date are required.');
      return;
    }

    try {
      const response = await axios.post('http://localhost:5000/api/medicinereminder/reminder', {
        medicine_name: medicineName,
        dosage,
        timing,
        frequency,
        notes,
        start_date: startDate,
        end_date: endDate,
      }, { withCredentials: true });

      if (response.status === 201) {
        setMessage('Medicine reminder added successfully.');
        setMedicineName('');
        setDosage('');
        setTiming('');
        setFrequency('');
        setNotes('');
        setStartDate('');
        setEndDate('');
        setRefreshHistory(prev => !prev);

        // Trigger push notification test after adding reminder
        try {
          await axios.post('http://localhost:5000/api/medicinereminder/send_push', {}, { withCredentials: true });
          console.log('Push notification triggered after adding reminder.');
        } catch (err) {
          console.error('Failed to trigger push notification:', err);
        }
      } else {
        setError('Failed to add medicine reminder.');
      }
    } catch (err) {
      setError('Error: ' + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div className="medication-reminder-form">
      <h2>Add Medicine Reminder</h2>
      {message && <p className="success-message">{message}</p>}
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <label>
          Medicine Name*:
          <input
            type="text"
            value={medicineName}
            onChange={(e) => setMedicineName(e.target.value)}
            required
          />
        </label>
        <label>
          Dosage:
          <input
            type="text"
            value={dosage}
            onChange={(e) => setDosage(e.target.value)}
          />
        </label>
        <label>
          Timing:
          <input
            type="time"
            value={timing}
            onChange={(e) => setTiming(e.target.value)}
            placeholder="Select time"
          />
        </label>
        <label>
          Frequency:
          <input
            type="text"
            value={frequency}
            onChange={(e) => setFrequency(e.target.value)}
            placeholder="e.g., Daily, Twice a day"
          />
        </label>
        <label>
          Notes:
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
          />
        </label>
        <label>
          Start Date*:
          <input
            type="date"
            value={startDate}
            onChange={(e) => setStartDate(e.target.value)}
            required
          />
        </label>
        <label>
          End Date:
          <input
            type="date"
            value={endDate}
            onChange={(e) => setEndDate(e.target.value)}
          />
        </label>
        <button type="submit">Add Reminder</button>
      </form>
      <MedicationReminderHistory key={refreshHistory} />
    </div>
  );
};

export default MedicationReminderForm;
