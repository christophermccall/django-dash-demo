// import React from 'react';
// import ToastNotification from './components/ToastNotification';


// const App = () => {
//   return (
//     <div>
//       <h1>React Toast Notification Example</h1>
//       <ToastNotification />
//       <div className="container mt-5">
//         <h1 className="text-center">Pricing Plans</h1>
//         <div className="row">
//           <div className="col-md-4">
//             <div className="card">
//               <div className="card-body">
//                 <h5 className="card-title">Basic Plan</h5>
//                 <p className="card-text">$10/month</p>
//               </div>
//             </div>
//           </div>
//           <div className="col-md-4">
//             <div className="card">
//               <div className="card-body">
//                 <h5 className="card-title">Pro Plan</h5>
//                 <p className="card-text">$20/month</p>
//               </div>
//             </div>
//           </div>
//           <div className="col-md-4">
//             <div className="card">
//               <div className="card-body">
//                 <h5 className="card-title">Enterprise Plan</h5>
//                 <p className="card-text">$50/month</p>
//               </div>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// };

const App = () => {
  return (
    <div>
      <h1>React Toast Notification Example</h1>
      <ToastNotification />
    </div>
  );
};


// export default App;

// function App() {
//   return (
//     <div className="container mt-5">
//       <h1 className="text-center">Pricing Plans</h1>
//       <div className="row">
//         <div className="col-md-4">
//           <div className="card">
//             <div className="card-body">
//               <h5 className="card-title">Basic Plan</h5>
//               <p className="card-text">$10/month</p>
//             </div>
//           </div>
//         </div>
//         <div className="col-md-4">
//           <div className="card">
//             <div className="card-body">
//               <h5 className="card-title">Pro Plan</h5>
//               <p className="card-text">$20/month</p>
//             </div>
//           </div>
//         </div>
//         <div className="col-md-4">
//           <div className="card">
//             <div className="card-body">
//               <h5 className="card-title">Enterprise Plan</h5>
//               <p className="card-text">$50/month</p>
//             </div>
//           </div>
//         </div>
//       </div>
//     </div>
//   );
// }

// const App = () => {
//   return (
//     <div>
//       <h1>React Toast Notification Example</h1>
//       <ToastNotification />
//     </div>
//   );
// };
// export default App;

import React from 'react';
import { Toaster } from 'react-hot-toast';
import { toast } from "react-hot-toast";
import "react-hot-toast/dist/react-hot-toast.css";

function App() {
  return (
    <>
      <Toaster position="top-right" reverseOrder={false} />
      <h1>Welcome to Dashboard</h1>
      <button onClick={() => toast.success("This is a test toast!")}>
        Show Toast
      </button>
    </>
  );
}

export default App;