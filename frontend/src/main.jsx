import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import "./index.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

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

