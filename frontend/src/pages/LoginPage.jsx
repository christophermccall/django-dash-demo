import React from "react";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

const LoginPage = () => {
  const navigate = useNavigate();

  const handleLogin = () => {
    // Fake login logic
    navigate("/pricing");
  };

  return (
    <div className="container mt-5">
      <h1 className="text-center">Login Page</h1>
      <button className="btn btn-primary" onClick={handleLogin}>
        Log In
      </button>
    </div>
  );
};

export default LoginPage;

