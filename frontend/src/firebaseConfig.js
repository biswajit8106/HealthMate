import { initializeApp } from 'firebase/app';
import { getMessaging } from 'firebase/messaging';

const firebaseConfig = {
  
  apiKey: "AIzaSyA9T7KVEhq_KskSajDNskhaN1qR2XX-ci8",
  authDomain: "healthmate-413a7.firebaseapp.com",
  projectId: "healthmate-413a7",
  storageBucket: "healthmate-413a7.firebasestorage.app",
  messagingSenderId: "67278443162",
  appId: "1:67278443162:web:e995365e95649231864523",
  measurementId: "G-5GGZZYCJGV"
};


const app = initializeApp(firebaseConfig);
const messaging = getMessaging(app);

export { messaging };
