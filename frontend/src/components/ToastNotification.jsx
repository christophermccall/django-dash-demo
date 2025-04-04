import React from 'react';
import toast, { Toaster } from 'react-hot-toast';

const ToastNotification = () => {
  const showToast = () => {
    toast.success('This is a success notification!', { duration: 4000 });
    toast.error('Error occurred!', { icon: '❌' });
  };

  return (
    <div>
      <button onClick={showToast} className="btn btn-primary">
        Show Toast
      </button>
      <Toaster position="top-right" reverseOrder={false} />
    </div>
  );
};

export default ToastNotification;

