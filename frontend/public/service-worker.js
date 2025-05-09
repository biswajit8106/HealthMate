// Basic service worker for push notifications

self.addEventListener('push', function(event) {
  let data = {};
  if (event.data) {
    data = event.data.json();
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
  event.notification.close();
  event.waitUntil(
    clients.matchAll({ type: 'window' }).then(function(clientList) {
      if (clients.openWindow) {
        return clients.openWindow('/');
      }
    })
  );
});
