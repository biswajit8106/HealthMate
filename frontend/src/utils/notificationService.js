import { messaging } from '../firebaseConfig';
import { getToken, onMessage, deleteToken } from 'firebase/messaging';
import axios from 'axios';

const VAPID_KEY = 'BOcghdVvM52WbIHQkTEpfVmB8vAgzVnLyJIcVp_tATRf506xMHPC88_arI2OQJxgllUCktOtFh1O7cnSbrYXEs4';

export const requestNotificationPermissionAndSendToken = async (userId) => {
  try {
    const permission = await Notification.requestPermission();
    if (permission === 'granted') {
      const currentToken = await getToken(messaging, { vapidKey: VAPID_KEY });
      if (currentToken) {
        // Send token to backend
        await axios.post('http://localhost:5000/api/save-fcm-token', {
          user_id: userId,
          token: currentToken,
        });
      }
    }
  } catch (error) {
    console.error('Error getting notification permission or token:', error);
  }
};

export const subscribeToPushNotifications = async (userId) => {
  try {
    const permission = await Notification.requestPermission();
    if (permission !== 'granted') {
      console.warn('Notification permission not granted');
      return;
    }
    const currentToken = await getToken(messaging, { vapidKey: VAPID_KEY });
    if (currentToken) {
      await axios.post('http://localhost:5000/api/save-fcm-token', {
        user_id: userId,
        token: currentToken,
      });
      console.log('Subscribed to push notifications');
    }
  } catch (error) {
    console.error('Failed to subscribe to push notifications:', error);
  }
};

export const unsubscribeFromPushNotifications = async (userId) => {
  try {
    const currentToken = await getToken(messaging, { vapidKey: VAPID_KEY });
    if (currentToken) {
      // Delete token from Firebase Messaging
      await deleteToken(messaging);
      // Inform backend to delete token
      await axios.post('http://localhost:5000/api/delete-fcm-token', {
        user_id: userId,
        token: currentToken,
      });
      console.log('Unsubscribed from push notifications');
    }
  } catch (error) {
    console.error('Failed to unsubscribe from push notifications:', error);
  }
};

export const listenForForegroundMessages = (callback) => {
  onMessage(messaging, (payload) => {
    console.log('Message received. ', payload);
    // Explicitly show notification in foreground
    if (Notification.permission === 'granted') {
      const { title, body } = payload.notification || {};
      if (title && body) {
        new Notification(title, { body });
      }
    }
    if (callback) {
      callback(payload);
    }
  });
};
