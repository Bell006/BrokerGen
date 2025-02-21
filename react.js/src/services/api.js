import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:5000/api',
    withCredentials: true,
    xsrfCookieName: 'csrf_token',
    xsrfHeaderName: "x-csrftoken",
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
});

api.interceptors.request.use(config => {
    if (['post', 'put', 'delete', 'get'].includes(config.method.toLowerCase())) {
        const csrfToken = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrf_token='))
            ?.split('=')[1];

        if (csrfToken) {
            config.headers['x-csrftoken'] = csrfToken;
        }
    }
    return config;
}, error => {
    return Promise.reject(error);
});

export { api };