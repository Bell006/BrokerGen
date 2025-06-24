import 'bootstrap/dist/css/bootstrap.min.css';
import './Dashboard.css';

import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router';

import robot_icon from '../../assets/robot_icon.svg';
import loadingIcon from '../../assets/loadingAn.svg';
import { api } from '../../services/api';
import { useAuth } from '../../contexts/AuthContext.jsx';

import { ConfirmationModal } from '../../components/ConfirmationModal.jsx';
import { Toast, showToast } from '../../components/Toast.jsx';
import { Input } from '../../components/Input.jsx';
import { DownloadCard } from '../../components/DownloadCard.jsx';
import { Dropdown } from '../../components/Dropdown.jsx';
import { CategoryBtn } from '../../components/CategoryBtn.jsx';

function Dashboard() {

  const navigate = useNavigate();
  const { logout } = useAuth();

  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    creci: '',
    categories: []
  });

  const [enterpriseData, setEnterpriseData] = useState([]);
  const [generatedImages, setGeneratedImages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);
  const [selectedCity, setSelectedCity] = useState('');
  const [selectedEnterprise, setSelectedEnterprise] = useState('');

  // Filtra as categorias do empreendimento selecionado
  const selectedEnterpriseData = enterpriseData.find(
    item => item.id === selectedEnterprise && item.cidade === selectedCity
  );

  const availableCategories = selectedEnterpriseData?.categorias || [];
  const categoryLabels = selectedEnterpriseData?.legendas || [];

  // Filtra as opções de cidade para o dropdown
  const cityOptions = [...new Set(enterpriseData.map(item => item.cidade))]
  .map(city => ({ value: city, label: city }));

  // Filtra as opções de empreendimento para o dropdown
  const enterpriseOptions = selectedCity
    ? enterpriseData
        .filter(item => item.cidade === selectedCity)
        .map((item, index) => ({
          value: item.id,
          label: item.empreendimento,
        }))
    : [];

  const handleLogout = () => {
    logout();
    navigate('/login');
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
        showToast('Selecione no máximo 5 categorias por vez.', 'warning');
        return;
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
      showToast('Selecione ao menos uma categoria.', 'warning');
      return;
    }

    const selectedEnterpriseObj = selectedEnterpriseData;

    const dataToSubmit = {
      ...formData,
      city: selectedCity,
      enterprise: selectedEnterpriseObj ? selectedEnterpriseObj.empreendimento : '',
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
      showToast(error.response?.data?.message || 'Erro ao criar as imagens.', 'error', true);
    } finally {
      setLoading(false);
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };


  useEffect(() => {
    const fetchData = async () => {
      try {
        const res = await api.get('/get_data');
        setEnterpriseData(res.data);
      } catch (err) {
        console.error("Falha ao carregar os dados", err);
      }
    };

    fetchData();
  }, []);

  return (
    <div className="container-fluid">
      <Toast />
      <div className="row row_100">
        {/* Left Column (Header and Images) */}
        <div className="col-lg-6">
          <div className="d-lg-flex flex-column justify-content-between ms-auto left_col_db" style={{ height: '100%' }}>

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
                    <div className="row row_100">
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
        <div className="col-lg-6">
          <div className="card shadow right_col_db">
            <div className="card-body ">
              <form class='form_db' onSubmit={handleSubmit}>
                <div className="inputs_form_db">
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

                    <label className="form-label mb-2">Categorias:</label>

                  <div className="d-flex justify-content-center align-items-center w-100">
                    {!selectedCity || !selectedEnterprise ? (
                      <p className="text-secondary mt-1 text-center py-2">Selecione uma cidade e um empreendimento</p>
                    ) : (
                      <div className="row">
                        {availableCategories.map((value, idx) => (
                          <CategoryBtn
                            key={value}
                            id={`category-${value}`}
                            value={value}
                            checked={formData.categories.includes(value)}
                            onChange={handleChange}
                            label={categoryLabels[idx] || value}
                          />
                        ))}
                      </div>
                    )}
                  </div>
                </div>
                
                <button
                  type="submit"
                  className="btn btn-primary w-100 submit_btn_db mt-4"
                  disabled={loading || formData.categories.length === 0 || !selectedCity || !selectedEnterprise || formData.name === '' || formData.phone === '' || formData.creci === ''}
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
