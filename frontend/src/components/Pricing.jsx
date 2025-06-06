import React from 'react';

const Pricing = () => {
  return (
    <div>
      <div className="container mt-5">
      <h1 className="text-center mb-5 text-primary">Our Pricing Plans</h1>
<div className="row text-center">
  <div className="col-md-4">
    <div className="card shadow-lg border-0 rounded-lg">
      <div className="card-body">
        <h5 className="card-title mb-4 text-success">Core Membership</h5>
        <p className="card-text lead">$10/month</p>
        <p className="text-muted mb-4">
          Includes access to our core platform and up to 20 API calls for free.
        </p>
        <p className="text-muted mb-4">
          After 20 calls, it's $0.05 per call until 50 calls. After 50 calls, it's $0.03 per call.
        </p>
        <button className="btn btn-outline-success btn-lg">Get Started</button>
      </div>
    </div>
  </div>

  <div className="col-md-4">
    <div className="card shadow-lg border-0 rounded-lg">
      <div className="card-body">
        <h5 className="card-title mb-4 text-primary">Pro Plan</h5>
        <p className="card-text lead">$20/month</p>
        <p className="text-muted mb-4">Ideal for growing businesses. Includes extra features.</p>
        <button className="btn btn-outline-primary btn-lg">Sign Up</button>
      </div>
    </div>
  </div>

  <div className="col-md-4">
    <div className="card shadow-lg border-0 rounded-lg">
      <div className="card-body">
        <h5 className="card-title mb-4 text-danger">Enterprise Plan</h5>
        <p className="card-text lead">$50/month</p>
        <p className="text-muted mb-4">For larger teams with advanced needs, including unlimited API calls.</p>
        <button className="btn btn-outline-danger btn-lg">Contact Us</button>
      </div>
    </div>
  </div>
</div>
    </div>
    </div>
  );
};

export default Pricing;