import React, { useEffect, useRef, useState } from 'react';
import { Line } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from 'chart.js';
import 'bootstrap/dist/css/bootstrap.min.css';

// Register the necessary chart elements with Chart.js
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const UserEngagementGraph = () => {
  const [data, setData] = useState(null);  // To hold the data for the graph
  const [loading, setLoading] = useState(true);  // Loading state for the graph
  const [error, setError] = useState(null);  // Error state

  useEffect(() => {
    // Fetch the login data when the component mounts
    fetch('/dashboard/api/logins-per-day/')
      .then(response => response.json())
      .then((loginData) => {
        const logins = loginData.data || [];

        if (!Array.isArray(logins)) {
          throw new Error("Invalid data format: Expected an array in 'data' field.");
        }

        // Prepare the data for the chart
        const labels = logins.map(item => item.login_date);
        const data = logins.map(item => item.login_count);

        setData({
          labels: labels,
          datasets: [
            {
              label: '# of Logins',
              data: data,
              borderColor: 'rgba(75, 192, 192, 1)',
              fill: false,
              borderWidth: 2
            }
          ]
        });
        setLoading(false);
      })
      .catch((error) => {
        setError('Error fetching login data');
        setLoading(false);
        console.error('Error fetching login data:', error);
      });
  }, []);

  if (loading) return <div>Loading...</div>; // Display loading state
  if (error) return <div>{error}</div>; // Display error message

  return (
    <div className="card shadow-lg border-0 rounded-lg">
      <div className="card-body">
        <h5 className="card-title mb-4 text-primary">User Engagement</h5>
        <p className="card-text lead mb-4"># of Logins</p>
        <Line data={data} options={{
          responsive: true,
          plugins: {
            title: {
              display: true,
              text: 'User Engagement Over Time',
            },
          },
          scales: {
            y: {
              beginAtZero: true,
            }
          }
        }} />
      </div>
    </div>
  );
};

export default UserEngagementGraph;
