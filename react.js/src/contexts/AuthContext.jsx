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
    const storedBroker = localStorage.getItem('broker');
    if (storedBroker) {
      setIsAuthenticated(true);
      setBroker(JSON.parse(storedBroker));
    }
  }, []);

  // Get CSRF Token
  const getCsrfToken = async () => {
    const tokenResponse = await api.get('/csrf-token', { withCredentials: true });
    return tokenResponse.data.csrf_token;
  };

  // Login method
  const login = async (brokerData) => {
    try {
      const csrfToken = await getCsrfToken();
      api.defaults.headers.common['X-CSRFToken'] = csrfToken;

      const response = await api.post('/login', brokerData, {
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        },
        withCredentials: true
      });

      localStorage.setItem('broker', JSON.stringify(response.data.broker));
      setIsAuthenticated(true);
      setBroker(response.data.broker);

      return response.data;
    } catch (error) {
      throw new Error(
          error.response?.data?.message || 
          'Falha ao fazer login'
      );
    }
  };

  const signup = async (signupData) => {
    try {
      const csrfToken = await getCsrfToken();
      api.defaults.headers.common['X-CSRFToken'] = csrfToken;

      const response = await api.post('/signup', signupData, {
        headers: {
          'X-CSRFToken': csrfToken,
          'Content-Type': 'application/json'
        },
        withCredentials: true
      });

      return response.data;
    } catch (error) {
      throw new Error(
          error.response?.data?.message || 
          'Erro ao criar cadastro'
      );
    }
  };

  // Logout method
  const logout = () => {
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
