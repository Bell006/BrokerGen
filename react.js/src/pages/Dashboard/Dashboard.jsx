import 'bootstrap/dist/css/bootstrap.min.css';
import './Dashboard.css';

import React, { useState } from 'react';
import { useNavigate } from 'react-router';

import robot_icon from '../../assets/robot_icon.svg';
import loadingIcon from '../../assets/loadingAn.svg';
import { api } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext.jsx';
import { data } from '../../constants/categoriesAndEnterprises.js';

import { ConfirmationModal } from '../../components/ConfirmationModal.jsx';
import { Input } from '../../components/Input.jsx';
import { DownloadCard } from '../../components/DownloadCard.jsx';
import { Dropdown } from '../../components/Dropdown.jsx';
import { CategoryBtn } from '../../components/CategoryBtn.jsx';

function Dashboard() {

  const navigate = useNavigate();
  const { logout } = useAuth();

  const { categories, enterprises } = data;

  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    creci: '',
    categories: []
  });


  const [generatedImages, setGeneratedImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedEnterprise, setSelectedEnterprise] = useState('');

  const normalizeString = (str) => {
    return str
      .normalize('NFD') 
      .replace(/[\u0300-\u036f]/g, '') 
      .replace(/\/[A-Z]{2}/i, '')
      .replace(/\s+/g, '')
      .toLowerCase();
  };

  // Filtra as categorias do empreendimento selecionado
  const availableCategories = selectedEnterprise
    ? enterprises[selectedCity]?.find(enterprise => enterprise.id === parseInt(selectedEnterprise))?.categories || []
    : [];

  // Filtra as opções de cidade para o dropdown
  const cityOptions = Object.keys(enterprises).map((city) => ({ value: city, label: city }));

  // Filtra as opções de empreendimento para o dropdown
  const enterpriseOptions = selectedCity
    ? enterprises[selectedCity].map((enterprise) => ({
      value: enterprise.id,
      label: enterprise.name,
    }))
    : [];

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

    const selectedEnterpriseObj = enterprises[selectedCity]?.find(
      (enterprise) => enterprise.id === parseInt(selectedEnterprise)
    );
    
    const dataToSubmit = {
      ...formData,
      city: normalizeString(selectedCity),
      enterprise: normalizeString(selectedEnterpriseObj?.name || '')
    };

    setShowModal(true);
    setFormData(dataToSubmit); 
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
          <div className="d-lg-flex flex-column justify-content-between " style={{ height: '100%' }}>

            {/* Header */}
            <div className="header-container">
              <div className="top-container d-flex align-items-center justify-content-between mb-4">
                <div className="logo-container d-flex align-items-center">
                  <img src={robot_icon} alt="Robot outline icon" className="robot_icon me-3" />
                  <div>
                    <h1 className="h3 mb-0 text-light" >Gerador de peças</h1>
                    <p className="mb-0" style={{ color: '#cef146' }}>Corretores</p>
                  </div>
                </div>
                <button
                  className="btn btn-sm btn-danger"
                  onClick={handleLogout}
                >
                  Sair
                </button>
              </div>

              <Dropdown
                label="Cidade:"
                options={cityOptions}
                value={selectedCity}
                onChange={(e) => {
                  setSelectedCity(e.target.value);
                  setSelectedEnterprise('');
                }}
                placeholder="Selecione uma cidade"
              />

              <Dropdown
                label="Empreendimento:"
                options={enterpriseOptions}
                value={selectedEnterprise}
                onChange={(e) => setSelectedEnterprise(e.target.value)}
                disabled={!selectedCity}
                placeholder="Selecione um empreendimento"
              />
            </div>

            {/* Images */}
            <div className="images-container">
              <div className="results-container">
                <div className="results-card d-flex align-items-center mt-2 p-3">
                  {generatedImages.length <= 0 && (
                    <p className="text-center w-100 m-0">
                      {loading ? <img src={loadingIcon} /> : 'Nenhuma peça gerada ainda.'}
                    </p>
                  )}
                  <div className="card-body card-body-scrollable">
                    <div className="row">
                      {generatedImages.map((image, index) => (
                        <div key={index} className="col-12 col-md-4 mb-3">
                          <DownloadCard
                            category={image.category}
                            feedImageUrl={image.feed_image_url}
                            storiesImageUrl={image.stories_image_url}
                          />
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
          <div className="card shadow card_body_db">
            <div className="card-body ">
              <form onSubmit={handleSubmit}>
                <Input
                  label="Nome:"
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Maria da Silva"
                  required
                />

                <Input
                  label="Celular:"
                  type="text"
                  name='phone'
                  value={formData.phone}
                  onChange={handleChange}
                  placeholder="(64) 9 5647-7582"
                  mask
                  required
                />

                <Input
                  type="number"
                  className="form-control"
                  label="CRECI:"
                  name="creci"
                  value={formData.creci}
                  onChange={handleChange}
                  placeholder='45287'
                  required
                />

<div className="mb-3">
  <label className="form-label">Categorias:</label>

  {!selectedCity || !selectedEnterprise ? (
    <p className="text-secondary mt-1 text-center py-2">Selecione uma cidade e um empreendimento</p>
  ) : (
    <div className="row">
      {categories
        .filter(category => availableCategories.includes(category.value))
        .map((category) => (
          <CategoryBtn
            key={category.value}
            id={`category-${category.value}`}
            value={category.value}
            checked={formData.categories.includes(category.value)}
            onChange={handleChange}
            label={category.label}
          />
        ))}
    </div>
  )}
</div>

                <button
                  type="submit"
                  className="btn btn-primary w-100"
                  disabled={loading}
                >
                  {loading ? 'Aguarde...' : <span>Gerar peças</span>}
                </button>
              </form>
            </div>
          </div>
        </div>
      </div>

      <ConfirmationModal
        show={showModal}
        onClose={handleCloseModal}
        onConfirm={handleConfirmSubmit}
      />
    </div>
  );
}

export default Dashboard;
