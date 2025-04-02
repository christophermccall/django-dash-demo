// src/index.js
import React from 'react';
import ReactDOM from 'react-dom';
import App from './App';  // Import the App component

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root') // This will render inside the <div id="root"></div> in login.html
);
