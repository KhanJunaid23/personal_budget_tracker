import React, { useState, useEffect } from 'react';
import api from '../utils/api';

const TransactionForm = ({ onSuccess, transaction = null }) => {
  const [formData, setFormData] = useState({
    amount: transaction?.amount || '',
    category: transaction?.category?.id || '',
    detail: transaction?.detail || '',
    date: transaction?.date || new Date().toISOString().split('T')[0],
    type: transaction?.category?.type || 'income'
  });

  const [categories, setCategories] = useState([]);
  const [filteredCategories, setFilteredCategories] = useState([]);

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await api.get('api/v1/categories/');
        setCategories(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchCategories();
  }, []);

  useEffect(() => {
    setFilteredCategories(categories.filter(cat => cat.type === formData.type));
    if (transaction?.category?.type !== formData.type) {
      setFormData(prev => ({ ...prev, category: '' }));
    }
  }, [formData.type, categories, transaction]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        amount: formData.amount,
        category: parseInt(formData.category),
        detail: formData.detail,
        date: formData.date,
      };
      
      const response = transaction 
        ? await api.put(`api/v1/transactions/${transaction.id}/`, data)
        : await api.post('api/v1/transactions/', data);
      
      if (response.status >= 200 && response.status < 300) {
        onSuccess();
      } else {
        throw new Error('Failed to save transaction');
      }
    } catch (err) {
      console.error('Error saving transaction:', err);
      alert('Error saving transaction. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-4">
      <div className="row">
        <div className="col-md-3">
          <div className="form-group">
            <label>Amount</label>
            <input
              type="number"
              name="amount"
              className="form-control"
              value={formData.amount}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        <div className="col-md-3">
          <div className="form-group">
            <label>Type</label>
            <select
              name="type"
              className="form-control"
              value={formData.type}
              onChange={handleChange}
              required
            >
              <option value="income">Income</option>
              <option value="expense">Expense</option>
            </select>
          </div>
        </div>
        <div className="col-md-3">
          <div className="form-group">
            <label>Category</label>
            <select
              name="category"
              className="form-control"
              value={formData.category}
              onChange={handleChange}
              required
            >
              <option value="">Select Category</option>
              {filteredCategories.map(cat => (
                <option key={cat.id} value={cat.id}>{cat.name}</option>
              ))}
            </select>
          </div>
        </div>
        <div className="col-md-3">
          <div className="form-group">
            <label>Date</label>
            <input
              type="date"
              name="date"
              className="form-control"
              value={formData.date}
              onChange={handleChange}
              required
            />
          </div>
        </div>
      </div>
      <div className="form-group mt-2">
        <label>Description</label>
        <textarea
          name="detail"
          className="form-control"
          value={formData.detail}
          onChange={handleChange}
          rows="2"
        />
      </div>
      <button type="submit" className="btn btn-primary mt-2">
        {transaction ? 'Update' : 'Add'} Transaction
      </button>
    </form>
  );
};

export default TransactionForm;