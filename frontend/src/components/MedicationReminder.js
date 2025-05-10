import React, { useState, useEffect } from 'react';
import '../style/components/MedicationReminder.css';
import Navbar from './Navbar';

import axios from 'axios';
import { requestNotificationPermissionAndSendToken, subscribeToPushNotifications, unsubscribeFromPushNotifications } from '../utils/notificationService';

const MedicationReminder = ({ onClose }) => {
  const [medicineName, setMedicineName] = useState('');
  const [dosage, setDosage] = useState('');
  const [reminderTimes, setReminderTimes] = useState(['']);
  const [frequency, setFrequency] = useState('Daily');
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');
  const [upcomingReminders, setUpcomingReminders] = useState([]);
  const [userId, setUserId] = useState(null);
  const [isSubscribed, setIsSubscribed] = useState(false);

  const fetchSessionInfo = async () => {
    try {
      const response = await axios.get('http://localhost:5000/session', { withCredentials: true });
      if (response.data && response.data.user && response.data.user.user_id) {
        setUserId(response.data.user.user_id);
      }
    } catch (error) {
      console.error('Error fetching session info:', error);
    }
  };

  const fetchUpcomingReminders = async () => {
    if (!userId) return;
    try {
      const response = await axios.get(`http://localhost:5000/api/medication-reminder?user_id=${userId}`);
      setUpcomingReminders(response.data.reminders || []);
    } catch (error) {
      console.error('Error fetching upcoming reminders:', error);
    }
  };

  useEffect(() => {
    fetchSessionInfo();
  }, []);

  useEffect(() => {
    if (userId) {
      requestNotificationPermissionAndSendToken(userId);
      fetchUpcomingReminders();
    }
  }, [userId]);

  const handleReminderTimeChange = (index, value) => {
    const newTimes = [...reminderTimes];
    newTimes[index] = value;
    setReminderTimes(newTimes);
  };

  const addReminderTime = () => {
    setReminderTimes([...reminderTimes, '']);
  };

  const removeReminderTime = (index) => {
    const newTimes = reminderTimes.filter((_, i) => i !== index);
    setReminderTimes(newTimes);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!userId) {
      alert('User not logged in');
      return;
    }
    const reminderData = {
      user_id: userId,
      medicineName,
      dosage,
      reminderTimes: reminderTimes.filter(time => time),
      frequency,
      startDate,
      endDate,
    };
    try {
      await axios.post('http://localhost:5000/api/medication-reminder', reminderData);
      alert('Medication reminder saved successfully');
      // Refresh upcoming reminders after save
      fetchUpcomingReminders();
    } catch (error) {
      console.error('Error saving medication reminder:', error);
      alert('Failed to save medication reminder');
    }
  };

  const handleSubscribe = async () => {
    if (!userId) {
      alert('User not logged in');
      return;
    }
    await subscribeToPushNotifications(userId);
    setIsSubscribed(true);
  };

  const handleUnsubscribe = async () => {
    if (!userId) {
      alert('User not logged in');
      return;
    }
    await unsubscribeFromPushNotifications(userId);
    setIsSubscribed(false);
  };

  return (
    <div className="page-wrapper">
      <Navbar />
    <div className="medication-reminder-modal">
      <div className="medication-reminder-content">
        <h2>Add Medication Reminder</h2>
        <form onSubmit={handleSubmit}>
          <label>
            Medicine Name:
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
              required
            />
          </label>
          <label>
            Reminder Time(s):
            {reminderTimes.map((time, index) => (
              <div key={index} className="reminder-time-input">
                <input
                  type="time"
                  value={time}
                  onChange={(e) => handleReminderTimeChange(index, e.target.value)}
                  required
                />
                {reminderTimes.length > 1 && (
                  <button type="button" onClick={() => removeReminderTime(index)}>
                    Remove
                  </button>
                )}
              </div>
            ))}
            <button type="button" onClick={addReminderTime}>Add Time</button>
          </label>
          <label>
            Frequency:
            <select value={frequency} onChange={(e) => setFrequency(e.target.value)}>
              <option value="Daily">Daily</option>
              <option value="Weekly">Weekly</option>
              <option value="Monthly">Monthly</option>
            </select>
          </label>
          <label>
            Start Date:
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
              required
            />
          </label>
          <div className="form-buttons">
            <button type="submit">Save Reminder</button>
            <button type="button" onClick={onClose}>Cancel</button>
          </div>
        </form>
        <div className="subscription-controls">
          {isSubscribed ? (
            <button onClick={handleUnsubscribe}>Unsubscribe from Notifications</button>
          ) : (
            <button onClick={handleSubscribe}>Subscribe to Notifications</button>
          )}
        </div>
        <div className="upcoming-reminders">
          <h3>Upcoming Reminders</h3>
          {upcomingReminders.length === 0 ? (
            <p>No upcoming reminders.</p>
          ) : (
            <ul>
              {upcomingReminders.map((reminder) => (
                <li key={reminder.id}>
                  <strong>{reminder.medicineName}</strong> - {reminder.dosage} - Times: {reminder.reminderTimes.join(', ')} - Frequency: {reminder.frequency} - From {reminder.startDate} to {reminder.endDate}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
    </div>
  );
};

export default MedicationReminder;
