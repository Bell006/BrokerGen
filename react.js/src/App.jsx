import React, { useState } from 'react';
import InputMask from "react-input-mask";
import { FaDownload } from "react-icons/fa6";
import './App.css';
import { api } from './services/api';

function App() {
  const [formData, setFormData] = useState({
    name: '',
    phone: '',
    creci: '',
    categories: []
  });

  const [generatedImages, setGeneratedImages] = useState([]);
  const [loading, setLoading] = useState(false);
  
  const categories = [
    { value: 'condicoes1', label: 'Condições - 1' },
    { value: 'condicoes2', label: 'Condições - 2' },
    { value: 'general', label: 'Geral' },
    { value: 'investidor', label: 'Investidor' },
    { value: 'localizacao', label: 'Localização' },
    { value: 'petplace', label: 'Pet Place' },
    { value: 'playground', label: 'Playground' },
    { value: 'poliesportiva', label: 'Quadra poliesportiva' },
    { value: 'quadraAreia', label: 'Quadra de areia' },
  ];


  let digit = /[0-9]/;
  let mobileMask = ['(', digit, digit, ')', ' ', '9', ' ', digit, digit, digit, digit, '-', digit, digit, digit, digit];

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;

    if (type === "checkbox") {
      setFormData(prevState => {
        const updatedCategories = checked
          ? [...prevState.categories, value]
          : prevState.categories.filter(category => category !== value);

        return {
          ...prevState,
          categories: updatedCategories
        };
      });
    } else {
      setFormData(prevState => ({
        ...prevState,
        [name]: value
      }));
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      setGeneratedImages([]);

      const response = await api.post('/create_image', formData, {
        headers: {
          'Content-Type': 'application/json'
        }
      });

      if (response.status === 200) {
        setGeneratedImages(response.data.generated_images || []);
      } else {
        alert(`${response.data.message}`);
      }
    } catch (error) {
      console.log('Error details:', error);
      if (error.response && error.response.data && error.response.data.message) {
        alert(error.response.data.message);
      } else if (error.request) {
        alert('A requisição foi feita, mas não houve resposta. Verifique a configuração do servidor.');
      } else {
        alert('Erro ao criar as imagens. Por favor, tente novamente mais tarde.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <div className="app-wrapper">

        <h1>Gerador de peças - Corretores</h1>
        <form onSubmit={handleSubmit}>

          <div className="inputWrapper">
            <label>
              Nome e sobrenome:
            </label>
            <input type="text" name="name" value={formData.name} onChange={handleChange} placeholder='Ex: Maria da Silva' required />
          </div>

          <div className="inputWrapper">
            <label>
              Celular:
            </label>
              <InputMask type='text' name='phone' value={formData.phone} onChange={handleChange} mask={mobileMask} required/>
          </div>

          <div className="inputWrapper">
            <label>
              CRECI:
            </label>
            <input type="number" name="creci" value={formData.creci} onChange={handleChange} placeholder='Ex: 99999' required />
          </div>


          <div className="inputWrapper">
            <label>Categorias:</label>
            <div className="checkboxGroup">
              {categories.map(category => (
                <label key={category.value}>
                  <input
                    type="checkbox"
                    value={category.value}
                    checked={formData.categories.includes(category.value)}
                    onChange={handleChange}
                  />
                  {category.label}
                </label>
              ))}
            </div>
          </div>

          <button type="submit" className="createButton" disabled={loading}>
            {loading ? 'Aguarde...' : 'Gerar peças'}
          </button>
        </form>

        {generatedImages.length > 0 && (
          <div className="results">
            <h2>Imagens Geradas</h2>
            <div className="imagesContainer">
              {generatedImages.map((image, index) => (
                <div key={index} className="imageCard">
                  <h3>{image.category}</h3>
                  <div className="imageLinks">
                    <a
                      href={image.feed_image_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="downloadButton"
                    >
                      <FaDownload /> Feed 
                    </a>
                    <a
                      href={image.stories_image_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="downloadButton"
                    >
                      <FaDownload /> Stories
                    </a>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

export default App;