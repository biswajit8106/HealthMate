// Basic service worker for push notifications

self.addEventListener('push', function(event) {
  console.log('[Service Worker] Push Received.');
  let data = {};
  if (event.data) {
    try {
      data = event.data.json();
    } catch (e) {
      console.warn('Push event data is not JSON, using text instead');
      data = { title: 'Medication Reminder', body: event.data.text() };
    }
    console.log('[Service Worker] Push data:', data);
  }
  const title = data.title || 'Medication Reminder';
  const options = {
    body: data.body || 'You have a medication reminder.',
    icon: '/logo192.png',
    badge: '/logo192.png'
  };
  event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function(event) {
  console.log('[Service Worker] Notification click Received.');
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(function(clientList) {
      if (clients.openWindow) {
        return clients.openWindow('/');
      }
    })
  );
});
