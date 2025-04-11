import React, { useEffect } from "react";
import { toast } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";
import { useLocation } from "react-router-dom";

import ToastNotification from './ToastNotification';


// Initialize toast notifications
// toast.configure();


// const ToastNotification = () => {
//     const location = useLocation();

//     useEffect(() => {
//         const params = new URLSearchParams(location.search);
//         const message = params.get("message");
//         const type = params.get("type");

//         if (message) {
//             switch (type) {
//                 case "success":
//                     toast.success(message, { position: toast.POSITION.TOP_RIGHT });
//                     break;
//                 case "error":
//                     toast.error(message, { position: toast.POSITION.TOP_RIGHT });
//                     break;
//                 case "warning":
//                     toast.warn(message, { position: toast.POSITION.TOP_RIGHT });
//                     break;
//                 default:
//                     toast.info(message, { position: toast.POSITION.TOP_RIGHT });
//                     break;
//             }
//         }
//     }, [location]);

//     return null;
// };

// export default ToastNotification;

export const notifySuccess = (message) => {
    toast.success(message, {
      position: toast.POSITION.TOP_RIGHT,
      autoClose: 3000,
      closeButton: false,
    });
  };
  
  export const notifyError = (message) => {
    toast.error(message, {
      position: toast.POSITION.TOP_RIGHT,
      autoClose: 3000,
      closeButton: false,
    });
  };
  
  export default { notifySuccess, notifyError };