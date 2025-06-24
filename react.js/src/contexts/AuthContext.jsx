import React, { createContext, useState, useContext, useEffect } from 'react';
import { api } from '../services/api';

// Create the AuthContext
export const AuthContext = createContext({
  isAuthenticated: false,
  broker: null,
  login: () => { },
  signup: () => { },
  logout: () => { }
});

// AuthProvider component
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [broker, setBroker] = useState(null);

  // Check authentication on initial load
  useEffect(() => {
    const validateUser = async () => {
      const token = localStorage.getItem('token');
      if (!token) {
        logout();
        return;
      }

      try {
        await api.get('/validate-token', {
          headers: {
            Authorization: `Bearer ${token}`
          }
        });

        const storedBroker = localStorage.getItem('broker');
        if (storedBroker) {
          setIsAuthenticated(true);
          setBroker(JSON.parse(storedBroker));
        }
      } catch (error) {
        logout();
        if (error.response?.status === 401) {
          logout();
          showToast('Sessão expirada. Faça login novamente.', 'error');
        }
      }
    };

    validateUser();
  }, []);

  // Login method
  const login = async (brokerData) => {
    try {
      const response = await api.post('/login', brokerData);
      localStorage.setItem('token', response.data.token);
      localStorage.setItem('broker', JSON.stringify(response.data.broker));
      setIsAuthenticated(true);
      setBroker(response.data.broker);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.message || 'Falha ao fazer login');
    }
  };

  const signup = async (signupData) => {
    try {
      const response = await api.post('/signup', signupData);
      localStorage.setItem('token', response.data.token);
      return response.data;
    } catch (error) {
      console.log('Signup Error Details:', error.response?.data);
      throw new Error(
        error.response?.data?.message ||
        'Erro ao criar cadastro'
      );
    }
};

  // Logout method
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('broker');
    setIsAuthenticated(false);
    setBroker(null);
  };

  return (
    <AuthContext.Provider value={{
      isAuthenticated,
      broker,
      login,
      signup,
      logout
    }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
