const publicVapidKey = "BOcghdVvM52WbIHQkTEpfVmB8vAgzVnLyJIcVp_tATRf506xMHPC88_arI2OQJxgllUCktOtFh1O7cnSbrYXEs4"; // Use the same VAPID public key as backend

// Convert base64 public key to Uint8Array
function urlBase64ToUint8Array(base64String) {
  const padding = '='.repeat((4 - base64String.length % 4) % 4);
  const base64 = (base64String + padding)
    .replace(/-/g, '+')
    .replace(/_/g, '/');

  const rawData = window.atob(base64);
  const outputArray = new Uint8Array(rawData.length);

  for (let i = 0; i < rawData.length; ++i) {
    outputArray[i] = rawData.charCodeAt(i);
  }
  return outputArray;
}

export async function registerServiceWorkerAndSubscribe() {
  if ('serviceWorker' in navigator && 'PushManager' in window) {
    try {
      // Register service worker
      const registration = await navigator.serviceWorker.register('/service-worker.js');
      console.log('Service Worker registered');

      // Request notification permission
      const permission = await Notification.requestPermission();
      if (permission !== 'granted') {
        console.log('Notification permission denied');
        return;
      }

      // Subscribe to push
      const subscription = await registration.pushManager.subscribe({
        userVisibleOnly: true,
        applicationServerKey: urlBase64ToUint8Array(publicVapidKey)
      });

      console.log('Push subscription:', subscription);

      // Send subscription to backend
      const response = await fetch('http://localhost:5000/api/medicinereminder/subscribe', {
        method: 'POST',
        credentials: 'include',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(subscription)
      });

      if (response.ok) {
        console.log('Push subscription saved on server');
      } else {
        console.error('Failed to save push subscription on server');
      }
    } catch (error) {
      console.error('Error during service worker registration or push subscription', error);
    }
  } else {
    console.warn('Service workers or Push messaging not supported');
  }
}
