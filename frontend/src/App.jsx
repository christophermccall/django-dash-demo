import React from 'react';

function App() {
  return (
    <div className="container mt-5">
      <h1 className="text-center">Pricing Plans</h1>
      <div className="row">
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Basic Plan</h5>
              <p className="card-text">$10/month</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Pro Plan</h5>
              <p className="card-text">$20/month</p>
            </div>
          </div>
        </div>
        <div className="col-md-4">
          <div className="card">
            <div className="card-body">
              <h5 className="card-title">Enterprise Plan</h5>
              <p className="card-text">$50/month</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
