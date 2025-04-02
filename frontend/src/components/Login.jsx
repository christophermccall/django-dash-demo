import React, { useState } from "react";
import { notifySuccess, notifyError } from "./ToastNotification";
import ToastNotification from "./ToastNotification";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      // Simulating API request (Replace with real API)
      const response = await fetch("/api/login", {
        method: "POST",
        body: JSON.stringify({ email, password }),
        headers: { "Content-Type": "application/json" },
      });

      if (response.ok) {
        notifySuccess("Login successful! Redirecting...");
      } else {
        notifyError("Invalid credentials. Try again.");
      }
    } catch (error) {
      notifyError("Something went wrong!");
    }
  };

  return (
    <div>
      <form onSubmit={handleLogin}>
        <h3>Login Here</h3>
        <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Login</button>
      </form>

      <ToastNotification />
    </div>
  );
};

export default Login;
