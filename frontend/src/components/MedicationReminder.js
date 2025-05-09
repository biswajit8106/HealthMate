import React, { useState } from 'react';
import { registerServiceWorkerAndSubscribe } from '../serviceWorkerRegistration';

const MedicationReminder = () => {
  const [permission, setPermission] = useState(Notification.permission);
  const [subscriptionStatus, setSubscriptionStatus] = useState(null);

  const handleSubscribe = async () => {
    if (permission === 'granted') {
      setSubscriptionStatus('Already subscribed');
      return;
    }
    if (permission === 'denied') {
      alert('Notification permission was denied. Please enable it in your browser settings.');
      return;
    }
    try {
      await registerServiceWorkerAndSubscribe();
      setPermission(Notification.permission);
      setSubscriptionStatus('Subscribed successfully');
    } catch (error) {
      console.error('Subscription failed:', error);
      setSubscriptionStatus('Subscription failed');
    }
  };

  return (
    <div>
      <h3>Medication Reminder Push Notifications</h3>
      <p>Notification permission status: {permission}</p>
      <button onClick={handleSubscribe}>Enable Push Notifications</button>
      {subscriptionStatus && <p>{subscriptionStatus}</p>}
    </div>
  );
};

export default MedicationReminder;
