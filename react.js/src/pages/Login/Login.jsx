import { useState } from 'react';
import { useNavigate } from "react-router";

import { Toast, showToast } from '../../components/Toast.jsx';
import { useAuth } from '../../contexts/AuthContext.jsx';
import { Input } from '../../components/Input.jsx';
import { FaRegArrowAltCircleRight } from "react-icons/fa";
import './Login.css';

function Login() {
  let navigate = useNavigate();
  const { login } = useAuth();

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

    try {
      const result = await login(loginData);

      if (result.broker) {
        navigate('/dashboard');
      } else {
        showToast(result.message || 'Falha ao fazer login', 'error', true);
      }
    } catch (error) {
      showToast(error.message || 'Falha ao fazer login', 'error', true);
    }
  };

  return (
    <>
      <Toast />
      <div className="login-container p-4">
        <div className="login-card">
          <div className="login-header">
            <h1 className="login-title h3">Login</h1>
            <p className="login-subtitle">Corretores</p>
          </div>
          <form className="login-form" onSubmit={handleSubmit}>
            <Input
              label="Email:"
              type="email"
              name="email"
              value={loginData.email}
              onChange={handleChange}
              placeholder="email@exemplo.com"
              required
            />

            <Input
              label="Cód. UAU"
              type="text"
              name="code_uau"
              value={loginData.code_uau}
              onChange={handleChange}
              placeholder="45287"
              required
            />

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
                  <FaRegArrowAltCircleRight />
                </a>
              </div>
            </div>
          </form>
        </div>
      </div>
    </>
  );
}

export default Login;
