import { initializeApp } from 'firebase/app';
import { getMessaging } from 'firebase/messaging';

const firebaseConfig = {
  apiKey: "AIzaSyBF0r47tyhUilgh-ZTVG-s4mn3-zhRQHhU",
  authDomain: "healthmate-4ef24.firebaseapp.com",
  projectId: "healthmate-4ef24",
  storageBucket: "healthmate-4ef24.firebasestorage.app",
  messagingSenderId: "267796350393",
  appId: "1:267796350393:web:d349ef627931e24ed3a268",
  measurementId: "G-X45Q1ESRQJ"
};

const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

export { messaging };
