import React, { useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ToastContainer, toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import ToastNotification from "./components/ToastNotification.jsx";
import LoginPage from "./pages/LoginPage";
import PricingPage from "./pages/PricingPage";
// import Login from "./components/Login";
import Signup from "./components/Signup";

const App = () => {
  // useEffect(() => {
  //   toast.success("Welcome to the Dashboard!", { position: "top-right" });
  // }, []);

  return (
    <Router>
       {/* <ToastNotification /> */}
      <ToastContainer autoClose={3000} hideProgressBar closeButton={false} />
      <Routes>
        {/* <Route path="/" element={<Login />} /> */}
        <Route path="/" element={<LoginPage />} />
        <Route path="/pricing" element={<PricingPage />} />
        <Route path="/signup" element={<Signup />} />
      </Routes>
    </Router>
  );
};

export default App;