
// import { StrictMode } from 'react';
// import { createRoot } from 'react-dom/client';
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import App from './App.jsx';

// createRoot(document.getElementById('react-root')).render(
//   <StrictMode>
//     <App />
//   </StrictMode>
// );
ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);

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

