import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import CategoryList from '../components/CategoryList';
import api from '../utils/api';

const CategoriesPage = () => {
  const [categories, setCategories] = useState([]);

  const fetchCategories = async () => {
    try {
      const res = await api.get('api/v1/categories/');
      setCategories(res.data);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchCategories();
  }, []);

  return (
    <>
      <Navbar />
      <div className="container mt-4">
        <h2 className="mb-4">Manage Categories</h2>
        <CategoryList
          categories={categories}
          onEdit={() => {}}
          onDelete={fetchCategories}
          onAddNew={fetchCategories}
        />
      </div>
    </>
  );
};

export default CategoriesPage;