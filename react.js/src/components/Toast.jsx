import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

export const Toast = () => {
  return (
    <ToastContainer
      position="top-right"
      hideProgressBar={false}
      closeOnClick={true}
      pauseOnHover={true}
      draggable={true}
    />
  );
};

export const showToast = (message, type, persist = false) => {
    const toastTypes = {
        success: toast.success,
        error: toast.error,
        info: toast.info,
        warning: toast.warning
      };
    
      const toastFunction = toastTypes[type] || toast.error;
    
      toastFunction(message, {
        position: "top-right",
        autoClose: persist ? false : 3000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
      });
};