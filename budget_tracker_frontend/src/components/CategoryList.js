import React, { useState } from 'react';
import api from '../utils/api';
import CategoryForm from './CategoryForm';

const CategoryList = ({ categories, onEdit, onDelete, onAddNew }) => {
  const [filterType, setFilterType] = useState('all');
  const [editingCategory, setEditingCategory] = useState(null);
  const [showForm, setShowForm] = useState(false);

  const filteredCategories = categories.filter(category => {
    if (filterType === 'all') return true;
    return category.type === filterType;
  });

  const handleDelete = async (id) => {
    try {
      await api.delete(`api/v1/categories/${id}/`);
      onDelete();
    } catch (err) {
      console.error(err);
    }
  };

  const handleSuccess = () => {
    setShowForm(false);
    setEditingCategory(null);
    onAddNew();
  };

  return (
    <div>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4>Categories</h4>
        <div>
          <select
            className="form-select me-2"
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
            style={{ width: 'auto', display: 'inline-block' }}
          >
            <option value="all">All Types</option>
            <option value="income">Income</option>
            <option value="expense">Expense</option>
          </select>
          <button
            className="btn btn-primary"
            onClick={() => {
              setEditingCategory(null);
              setShowForm(true);
            }}
          >
            Add Category
          </button>
        </div>
      </div>

      {showForm && (
        <div className="card mb-3">
          <div className="card-body">
            <CategoryForm
              category={editingCategory}
              onSuccess={handleSuccess}
              onCancel={() => setShowForm(false)}
            />
          </div>
        </div>
      )}

      <div className="table-responsive">
        <table className="table table-striped">
          <thead>
            <tr>
              <th>Name</th>
              <th>Type</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            {filteredCategories.map((category) => (
              <tr key={category.id}>
                <td>{category.name}</td>
                <td>
                  <span className={`badge ${category.type === 'income' ? 'bg-success' : 'bg-danger'}`}>
                    {category.type}
                  </span>
                </td>
                <td>
                  <button
                    className="btn btn-sm btn-warning me-2"
                    onClick={() => {
                      setEditingCategory(category);
                      setShowForm(true);
                    }}
                  >
                    Edit
                  </button>
                  <button
                    className="btn btn-sm btn-danger"
                    onClick={() => handleDelete(category.id)}
                  >
                    Delete
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CategoryList;