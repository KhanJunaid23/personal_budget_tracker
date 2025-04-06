import React, { useState } from 'react';
import api from '../utils/api';

const CategoryForm = ({ category = null, onSuccess, onCancel }) => {
  const [formData, setFormData] = useState({
    name: category?.name || '',
    type: category?.type || 'expense'
  });

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      if (category) {
        await api.put(`api/v1/categories/${category.id}/`, formData);
      } else {
        await api.post('api/v1/categories/', formData);
      }
      onSuccess();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="mb-3">
      <div className="row">
        <div className="col-md-6">
          <div className="form-group">
            <label>Category Name</label>
            <input
              type="text"
              name="name"
              className="form-control"
              value={formData.name}
              onChange={handleChange}
              required
            />
          </div>
        </div>
        <div className="col-md-6">
          <div className="form-group">
            <label>Type</label>
            <select
              name="type"
              className="form-control"
              value={formData.type}
              onChange={handleChange}
              required
            >
              <option value="expense">Expense</option>
              <option value="income">Income</option>
            </select>
          </div>
        </div>
      </div>
      <div className="mt-2">
        <button type="submit" className="btn btn-primary me-2">
          {category ? 'Update' : 'Add'} Category
        </button>
        {onCancel && (
          <button type="button" className="btn btn-secondary" onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
    </form>
  );
};

export default CategoryForm;