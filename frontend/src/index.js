import React from 'react';
import ReactDOM from 'react-dom/client';
import './style/styles.css';
import App from './App';
import { AuthProvider } from './context/AuthContext';
import './axiosConfig';
import { registerServiceWorkerAndSubscribe } from './serviceWorkerRegistration';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <AuthProvider>
      <App />
    </AuthProvider>
  </React.StrictMode>
);

registerServiceWorkerAndSubscribe();
