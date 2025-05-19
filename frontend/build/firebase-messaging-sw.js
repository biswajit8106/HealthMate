importScripts('https://www.gstatic.com/firebasejs/9.22.2/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.22.2/firebase-messaging-compat.js');

firebase.initializeApp({
   apiKey: "AIzaSyBF0r47tyhUilgh-ZTVG-s4mn3-zhRQHhU",
  authDomain: "healthmate-4ef24.firebaseapp.com",
  projectId: "healthmate-4ef24",
  storageBucket: "healthmate-4ef24.firebasestorage.app",
  messagingSenderId: "267796350393",
  appId: "1:267796350393:web:d349ef627931e24ed3a268",
  measurementId: "G-X45Q1ESRQJ"
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
