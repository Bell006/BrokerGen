import React, { useState } from 'react';
import { api } from '../../services/api';
import './Login.css';

function Login() {
  const [loginData, setLoginData] = useState({
    email: '',
    creci: ''
  });

  const [error, setError] = useState('');

  const handleChange = (e) => {
    const { name, value } = e.target;
    setLoginData({
      ...loginData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await api.post('/login', loginData);

      // Store user info in localStorage
      localStorage.setItem('broker', JSON.stringify(response.data.broker));
      
      // Force a full navigation
      window.location.href = '/dashboard';

    } catch (error) {
      console.error('Login error:', error);
      setError(error.response?.data?.message || 'Falha ao fazer login.');
    }
  };

  return (
    <div className="login-container gap-4">
      <div className="login-card">
        <div className="login-header">
          <h1 className="login-title h3">Login</h1>
          <p className="login-subtitle">Corretores</p>
        </div>
        <form className="login-form" onSubmit={handleSubmit}>
          <div className="mb-3">
            <label className="form-label">Email:</label>
            <input
              type="email"
              className="form-control"
              name="email"
              value={loginData.email}
              onChange={handleChange}
              placeholder='maria@exemplo.com'
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">CRECI:</label>
            <input
              type="text"
              className="form-control"
              name="creci"
              value={loginData.creci}
              onChange={handleChange}
              placeholder='45287'
              required
            />
          </div>

          <button
            type="submit"
            className="btn login-btn w-100"
          >
            Entrar
          </button>
        </form>
      </div>
      {error &&
          <div class="alert alert-danger" role="alert">
            {error}
          </div>}
    </div>
  );
}

export default Login;
