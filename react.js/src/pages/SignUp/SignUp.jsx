import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Toast, showToast } from '../../components/Toast.jsx';
import 'react-toastify/dist/ReactToastify.css';

import { useAuth } from '../../contexts/AuthContext.jsx';
import { Input } from '../../components/Input.jsx';
import loadingIcon from '../../assets/loadingAn.svg';
import { FaRegArrowAltCircleRight } from 'react-icons/fa';
import './SignUp.css';

function SignUp() {

  const navigate = useNavigate();
  const { signup } = useAuth();

  const [loading, setLoading] = useState(false);
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

    setLoading(true);

    try {
      const result = await signup(signUpData);

      if (result.broker) {
        showToast(result.message, 'success');
        setTimeout(() => {
          navigate('/login');
        }, 4000);
  
      } else {
        showToast(result.message || 'Erro ao criar cadastro', 'error', true);
      }
    } catch (error) {
      showToast(error.message || 'Erro ao criar cadastro', 'error', true);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="login-container p-4">
      <Toast />
        <div className="login-card">
          <div className="login-header">
            <h2 className="login-title h3 mb-0">Criar Conta</h2>
          </div>
          <form className="login-form" onSubmit={handleSubmit}>
            <Input
              label="Nome e sobrenome"
              type="text"
              name="name"
              value={signUpData.name}
              onChange={handleChange}
              placeholder="Maria da Silva"
              required
            />
            <Input
              label="Email"
              type="email"
              name="email"
              value={signUpData.email}
              onChange={handleChange}
              placeholder="corretor@exemplo.com"
              required
            />
            <Input
              label="Cód. UAU"
              type="text"
              name="code_uau"
              value={signUpData.code_uau}
              onChange={handleChange}
              placeholder="45819"
              required
            />
            <button
              type="submit"
              className="btn btn-primary w-100"
              disabled={loading}
            >
              {loading ? <img src={loadingIcon} className="loadingIcon" /> : "Cadastrar"}
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
    </>
  );
}

export default SignUp;
