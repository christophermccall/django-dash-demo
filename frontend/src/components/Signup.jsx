import React, { useState } from "react";
import { notifySuccess, notifyError } from "./ToastNotification"; // Import toast functions
import ToastNotification from "./ToastNotification"; // Import Toaster Component

const Signup = () => {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSignup = async (e) => {
    e.preventDefault();

    try {
      // Simulating API request (Replace with real API)
      const response = await fetch("/api/signup", {
        method: "POST",
        body: JSON.stringify({ username, email, password }),
        headers: { "Content-Type": "application/json" },
      });

      if (response.ok) {
        notifySuccess("Signup successful! Redirecting...");
      } else {
        notifyError("Signup failed. Try again.");
      }
    } catch (error) {
      notifyError("Something went wrong!");
    }
  };

  return (
    <div>
      <form onSubmit={handleSignup}>
        <h3>Signup Here</h3>
        <input type="text" placeholder="Username" onChange={(e) => setUsername(e.target.value)} />
        <input type="email" placeholder="Email" onChange={(e) => setEmail(e.target.value)} />
        <input type="password" placeholder="Password" onChange={(e) => setPassword(e.target.value)} />
        <button type="submit">Signup</button>
      </form>

      {/* <ToastNotification /> Render Toaster */}
    </div>
  );
};

export default Signup;
