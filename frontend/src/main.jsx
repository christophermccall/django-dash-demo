import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';
import Pricing from './components/Pricing';
import ToastNotification from './components/ToastNotification';

const root1 = document.getElementById('react-root');
const root2 = document.getElementById('react-pricing-root');
const root3 = document.getElementById('react-toast-root');

if (root1) {
  console.log("Mounting App on #react-root");
  ReactDOM.createRoot(root1).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("Failed to find #react-root");
}

if (root2) {
  console.log("Mounting Pricing on react-pricing-root");
  ReactDOM.createRoot(root2).render(
    <React.StrictMode>
      <Pricing />
    </React.StrictMode>
  );
} else {
  console.error("Failed to find #react-pricing-root");
}

if (root3) {
  console.log("Mounting ToastNotification on #react-toast-root");
  ReactDOM.createRoot(root3).render(
    <React.StrictMode>
      <ToastNotification />
    </React.StrictMode>
  );
} else {
  console.error("Failed to find #react-toast-root");
}