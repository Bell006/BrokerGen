import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext.jsx';
import './SignUp.css';
import { FaRegArrowAltCircleRight } from 'react-icons/fa';
import './SignUp.css';

function SignUp() {
  const navigate = useNavigate();
  const { signup } = useAuth();

  const [error, setError] = useState('');
  const [signUpData, setSignUpData] = useState({
    name: '',
    email: '',
    code_uau: ''
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setSignUpData({
      ...signUpData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const result = await signup(signUpData);

      if (result.broker) {
          alert(result.message || 'Cadastro realizado com sucesso');
        
          navigate('/login');
      } else {
          setError(result.message || 'Erro ao criar cadastro');
      }
  } catch (error) {
      console.error('Signup Submission Error:', error);
      setError(error.message || 'Erro ao criar cadastro');
  }
};

  return (
    <>
      <div className="login-container">
        <div className="login-card">
          <div className="login-header">
            <h2 className="login-title h3 mb-0">Criar Conta</h2>
          </div>
          <form className="login-form" onSubmit={handleSubmit}>
            <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
            <div className="mb-3">
              <label className="form-label">Nome e sobrenome</label>
              <input
                type="text"
                className="form-control"
                name="name"
                value={signUpData.name}
                onChange={handleChange}
                placeholder="Maria da Silva"
                required
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Email</label>
              <input
                type="email"
                className="form-control"
                name="email"
                value={signUpData.email}
                onChange={handleChange}
                placeholder="corretor@exemplo.com"
                required
              />
            </div>
            <div className="mb-3">
              <label className="form-label">Cód. UAU</label>
              <input
                type="text"
                className="form-control"
                name="code_uau"
                value={signUpData.code_uau}
                onChange={handleChange}
                placeholder="45819"
                required
              />
            </div>
            <button type="submit" className="btn btn-primary w-100">
              Cadastrar
            </button>

            <div className="signUp text-center d-flex flex-column align-items-center justify-content-center mt-2">
              <p className="text-muted small mb-0 mt-2">Já possui uma conta?</p>
              <div className="siginUp-wrapper">
                <a href="/login" className="signUp-link small d-flex align-items-center gap-1">
                  Login
                  <FaRegArrowAltCircleRight />
                </a>
              </div>
            </div>
          </form>
        </div>
      </div>
      {error &&
        <div className="login-error alert alert-danger text-center mt-4" role="alert">
          {error}
        </div>}
    </>
  );
}

export default SignUp;
