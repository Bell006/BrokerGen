import axios from 'axios';

const baseURL = import.meta.env.MODE === 'development'
    ? import.meta.env.VITE_API_URL // Development
    : import.meta.env.VITE_API_URL_PROD; // Production


const api = axios.create({
    baseURL,
    headers: {
        'Content-Type': 'application/json'
    }
});

api.interceptors.request.use(config => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

export { api };