import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/',
});

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('accessToken');

    if (
      !config.url.includes('/login/') &&
      !config.url.includes('/token/') &&
      !config.url.includes('/refresh/')
    ) {
      if (token) {
        config.headers['Authorization'] = `Bearer ${token}`;
        console.log('✅ Token attached:', token);
      }
    }

    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

export default api;
