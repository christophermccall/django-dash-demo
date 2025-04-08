import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';  // Ensure you have this CSS file or remove the import if unnecessary
import App from './App.jsx';  // Ensure App.js is present or change this to match your entry point
import { BrowserRouter as Router } from 'react-router-dom';

ReactDOM.render(
    <React.StrictMode>
      <Router>
        <App />
      </Router>
    </React.StrictMode>,
    document.getElementById('root')
  );

