import React, { useState, useEffect } from 'react';
import { useNavigate } from "react-router";
import { useAuth } from '../../contexts/AuthContext.jsx';
import { FaRegArrowAltCircleRight } from "react-icons/fa";
import './Login.css';

function Login() {
  let navigate = useNavigate();
  const { login } = useAuth();

  const [error, setError] = useState('');
  const [loginData, setLoginData] = useState({
    email: '',
    code_uau: ''
  });


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
        const result = await login(loginData);

        if (result.broker) {
            navigate('/dashboard');
        } else {
            setError(result.message || 'Falha ao fazer login');
        }
    } catch (error) {
        console.error('Login Submission Error:', error);
        setError(error.message);
    }
};

  return (
    <>
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
              placeholder='email@exemplo.com'
              required
            />
          </div>

          <div className="mb-3">
            <label className="form-label">Cód. UAU</label>
            <input
              type="text"
              className="form-control"
              name="code_uau"
              value={loginData.code_uau}
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

          <div className="signUp text-center d-flex flex-column align-items-center justify-content-center">
            <p className="text-muted small mb-0 mt-2">Não possui uma conta?</p>
            <div className="siginUp_wrapper">
              <a href="/signup" className="signUp-link small d-flex align-items-center gap-1"> 
                Cadastre-se
                <FaRegArrowAltCircleRight/>
              </a>
            </div>
          </div>
        </form>
      </div>
    </div>
    {error &&
          <div className="alert alert-danger text-center m-4" role="alert">
            {error}
          </div>}
    </> 
  );
}

export default Login;
