import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../utils/api';

const Login = () => {
  const [credentials, setCredentials] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem('accessToken');
    if (token) {
      navigate('/dashboard');
    }
  }, [navigate]);

  const handleChange = (e) => {
    setCredentials({ ...credentials, [e.target.name]: e.target.value });
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      let cred = {
        username: credentials.username,
        password: credentials.password,
      };
      const res = await api.post("/api/v1/auth/login/",cred);
      localStorage.setItem("accessToken", res.data.access);
      localStorage.setItem("refreshToken", res.data.refresh);

      navigate("/dashboard");
    } catch (err) {
      console.error(err);
      setError("Invalid credentials");
      alert("Invalid credentials");
    }
  };

  return (
    <div className="container mt-5">
      <h2 className="text-center mb-4">Login</h2>
      <form onSubmit={handleLogin} className="mx-auto" style={{ maxWidth: '400px' }}>
        {error && <div className="alert alert-danger">{error}</div>}
        <div className="form-group mb-3">
          <label>Username</label>
          <input type="text" name="username" className="form-control" onChange={handleChange} required />
        </div>
        <div className="form-group mb-3">
          <label>Password</label>
          <input type="password" name="password" className="form-control" onChange={handleChange} required />
        </div>
        <button type="submit" className="btn btn-primary w-100">Login</button>
      </form>
    </div>
  );
};

export default Login;
