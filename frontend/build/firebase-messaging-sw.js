importScripts('https://www.gstatic.com/firebasejs/9.22.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.22.2/firebase-messaging-compat.js');

firebase.initializeApp({
   apiKey: "AIzaSyA9T7KVEhq_KskSajDNskhaN1qR2XX-ci8",
  authDomain: "healthmate-413a7.firebaseapp.com",
  projectId: "healthmate-413a7",
  storageBucket: "healthmate-413a7.firebasestorage.app",
  messagingSenderId: "67278443162",
  appId: "1:67278443162:web:e995365e95649231864523",
  measurementId: "G-5GGZZYCJGV"
});

const messaging = firebase.messaging();

messaging.onBackgroundMessage(function(payload) {
  console.log('[firebase-messaging-sw.js] Received background message ', payload);
  const notificationTitle = payload.notification.title;
  const notificationOptions = {
    body: payload.notification.body,
    icon: '/firebase-logo.png'
  };

  self.registration.showNotification(notificationTitle, notificationOptions);
});
