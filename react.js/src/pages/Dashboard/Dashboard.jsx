import React, { useState } from 'react';
import InputMask from "react-input-mask";
import { useNavigate } from 'react-router';
import { FaDownload } from "react-icons/fa6";
import { api } from  '../../services/api';
import logo from '../../assets/Cidade-Buriti_logo.png';
import 'bootstrap/dist/css/bootstrap.min.css';
import './Dashboard.css';
import { useAuth } from '../../contexts/AuthContext.jsx';
import { Modal, Button } from 'react-bootstrap';
import loadingIcon from '../../assets/loadingAn.svg';

function Dashboard() {

  const navigate = useNavigate();
  const { logout } = useAuth();

  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    creci: '',
    categories: []
  });

  const [generatedImages, setGeneratedImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [subDivisionSelected, setsubDivisionSelected] = useState("");

  const categories = [
    { value: 'investidor', label: 'Investidor' },
    { value: 'localizacao', label: 'Localização' },
    { value: 'petplace', label: 'Pet Place' },
    { value: 'poliesportiva', label: 'Quadra poliesportiva' },
    { value: 'condicoes1', label: 'Condições - 1' },
    { value: 'condicoes2', label: 'Condições - 2' },
    { value: 'general', label: 'Geral' },
    { value: 'playground', label: 'Playground' },
    { value: 'quadraAreia', label: 'Quadra de areia' },
    { value: 'areaLazer', label: 'Área de lazer' },
  ];

  let digit = /[0-9]/;
  let mobileMask = ['(', digit, digit, ')', ' ', '9', ' ', digit, digit, digit, digit, '-', digit, digit, digit, digit];

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const handleApiError = (error) => {
    console.log('Error details:', error);
    alert(error.response?.data?.message || 'Erro ao criar as imagens.');
  };

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === 'checkbox') {
      const updatedCategories = checked
        ? formData.categories.includes(value) || formData.categories.length >= 5
          ? formData.categories
          : [...formData.categories, value]
        : formData.categories.filter((category) => category !== value);

      setFormData({
        ...formData,
        categories: updatedCategories,
      });

      if (checked && formData.categories.length >= 5) {
        alert('Selecione no máximo 5 categorias por vez.');
      }
    } else {
      setFormData({
        ...formData,
        [name]: value,
      });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (formData.categories.length === 0) {
      alert('Selecione ao menos uma categoria.');
      return;
    }

    setShowModal(true);
  };

  const handleConfirmSubmit = async (e) => {
    setShowModal(false);
    setLoading(true);

    try {
      setGeneratedImages([]);
      const response = await api.post('/create_image', formData, {
        headers: { 'Content-Type': 'application/json' }
      });

      setGeneratedImages(response.data.generated_images || []);
    } catch (error) {
      handleApiError(error);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <div className="container-fluid p-4">
      <div className="row">
        {/* Left Column (Header and Images) */}
        <div className="col-12 col-lg-6">
          <div className="d-lg-flex flex-column justify-content-between " style={{height: '100%'}}>

            {/* Header */}
            <div className="header-container">
              <div className="top-container d-flex align-items-center justify-content-between">
                <div className="logo-container d-flex align-items-center">
                  <img src={logo} alt="Logo" className="logo me-3"/>
                  <div>
                    <h1 className="h3 mb-0" style={{color: '#ffffff'}}>Gerador de peças</h1>
                    <p className="mb-0" style={{color: '#cef146'}}>Corretores</p>
                  </div>
                </div>
                  <button 
                  className="btn btn-sm btn-danger" 
                  onClick={handleLogout}
                  >
                  Logout
                  </button>
              </div>

              <div>
                <label className="subdivision-label mb-2 mt-4 ">Empreendimento:</label>
                <select
                  className="form-select"
                  aria-label="Default select example"
                  value={subDivisionSelected}
                  onChange={(e) => setsubDivisionSelected(e.target.value)}
                >
                  <option value="" disabled>Selecione um empreendimento</option>
                  <option value="1">Cidade Buriti</option>
                  <option value="2">Cidade Buriti</option>
                  <option value="3">Cidade Buriti</option>
                </select>
              </div>
            </div>
            
            {/* Images */}
            <div className="images-container">
                <div className="results-container">
                  <div className="results-card d-flex align-items-center mt-4 p-3">
                        {generatedImages.length <= 0 && (
                          <p className="text-center w-100 m-0">
                            {loading ? <img src={loadingIcon}/> : 'Nenhuma peça gerada ainda.'}
                          </p>
                        )}
                  <div className="card-body card-body-scrollable">
                      <div className="row">
                        {generatedImages.map((image, index) => (
                          <div key={index} className="col-12 col-md-4 mb-3">
                            <div className="card card-animated">
                              <div className="card-header">{image.category}</div>
                              <div className="card-body px-2 py-2">
                                <a
                                  href={image.feed_image_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="btn btn-outline-custom d-flex align-items-center mb-2"
                                >
                                  <FaDownload className="me-2" /> Feed
                                </a>
                                <a
                                  href={image.stories_image_url}
                                  target="_blank"
                                  rel="noopener noreferrer"
                                  className="btn btn-outline-custom d-flex align-items-center"
                                >
                                  <FaDownload className="me-2" /> Stories
                                </a>
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
            </div>
          </div>
        </div>

        {/* Right Column (Form) */}
        <div className="col-12 col-lg-6">
          <div className="card shadow">
            <div className="card-body">
              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label className="form-label">Nome:</label>
                  <input
                    type="text"
                    className="form-control"
                    name="name"
                    value={formData.name}
                    onChange={handleChange}
                    placeholder='Maria da Silva'
                    required
                  />
                </div>

                <div className="mb-3">
                  <label className="form-label">Celular:</label>
                  <InputMask
                    type='text'
                    className="form-control"
                    name='phone'
                    value={formData.phone}
                    onChange={handleChange}
                    mask={mobileMask}
                    placeholder='(64) 9 5647-7582'
                    required
                  />
                </div>

                <div className="mb-3">
                  <label className="form-label">CRECI:</label>
                  <input
                    type="number"
                    className="form-control"
                    name="creci"
                    value={formData.creci}
                    onChange={handleChange}
                    placeholder='45287'
                    required
                  />
                </div>

                <div className="mb-3">
                  <label className="form-label">Categorias:</label>
                  <div className="row">
                    {categories.map(category => (
                      <div key={category.value} className="col-6 col-md-4 mb-2">
                        <div className="form-check">
                          <input
                            type="checkbox"
                            className="form-check-input"
                            id={`category-${category.value}`}
                            value={category.value}
                            checked={formData.categories.includes(category.value)}
                            onChange={handleChange}
                          />
                          <label
                            className="form-check-label"
                            htmlFor={`category-${category.value}`}
                          >
                            {category.label}
                          </label>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>

                <button
                  type="submit"
                  className="btn btn-primary w-100"
                  disabled={loading}
                >
                  {loading ? 'Aguarde...' : <span className="fw-bold">Gerar peças</span>}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <Modal show={showModal} onHide={handleCloseModal} centered>
        <Modal.Header closeButton>
          <Modal.Title>Confirmação</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          Ao clicar em 'Entendi!', você concorda com o armazenamento das informações fornecidas para melhorias de navegação e análise de uso do site.
        </Modal.Body>
        <Modal.Footer>
          <Button variant="danger" onClick={handleCloseModal}>
            Cancelar
          </Button>
          <Button variant="primary" onClick={handleConfirmSubmit}>
            Entendi!
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default Dashboard;
