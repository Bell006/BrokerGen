import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const Toast = () => {
  return (
    <ToastContainer
      position="top-right"
      newestOnTop
      hideProgressBar={false}
      closeOnClick
      pauseOnHover
      draggable
    />
  );
};

export const showToast = (message, type = 'info') => {
  const toastTypes = {
    success: toast.success,
    error: toast.error,
    info: toast.info,
    warning: toast.warning,
  };

  const toastFunction = toastTypes[type] || toast.info;

  toastFunction(message, {
    hideProgressBar: false,
    closeOnClick: true,
    pauseOnHover: true,
    draggable: true,
  });
};