import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App';

const root = document.getElementById('react-root');

if (root) {
  console.log("✅ Mounting App on #react-root");
  ReactDOM.createRoot(root).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
} else {
  console.error("❌ Failed to find #react-root");
}