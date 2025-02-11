import React, { createContext, useState, useContext, useEffect } from 'react';

// Create the AuthContext
export const AuthContext = createContext({
  isAuthenticated: false,
  broker: null,
  login: () => {},
  logout: () => {}
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

  // Login method
  const login = (brokerData) => {
    localStorage.setItem('broker', JSON.stringify(brokerData));
    setIsAuthenticated(true);
    setBroker(brokerData);
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
      logout 
    }}>
      {children}
    </AuthContext.Provider>
  );
};


export const useAuth = () => useContext(AuthContext);
