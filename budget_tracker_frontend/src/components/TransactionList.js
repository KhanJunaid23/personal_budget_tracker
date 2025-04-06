import React, { useState, useEffect } from "react";
import api from "../utils/api";

const TransactionList = ({transactions,onEdit,onDelete,onPageChange,currentPage,totalPages}) => {
  const [filters, setFilters] = useState({
    category: "",
    startDate: "",
    endDate: "",
    minAmount: "",
    maxAmount: "",
  });
  const [categories, setCategories] = useState([]);

  const handleFilterChange = (e) => {
    setFilters({ ...filters, [e.target.name]: e.target.value });
  };

  const applyFilters = () => {
    onPageChange(1, filters);
  };

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await api.get("api/v1/categories/");
        setCategories(res.data);
      } catch (err) {
        console.error(err);
      }
    };
    fetchCategories();
  }, []);

  const clearFilters = () => {
    setFilters({
      category: "",
      startDate: "",
      endDate: "",
      minAmount: "",
      maxAmount: "",
    });
    onPageChange(1, {});
  };

  return (
    <div>
      <div className="card mb-4">
        <div className="card-header">
          <h5>Filters</h5>
        </div>
        <div className="card-body">
          <div className="row">
            <div className="col-md-3">
              <div className="form-group">
                <label>Category</label>
                <select
                  name="category"
                  className="form-control"
                  value={filters.category}
                  onChange={handleFilterChange}
                >
                  <option value="">All</option>
                  {categories.map((category) => (
                    <option key={category.id} value={category.id}>
                      {category.name}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div className="col-md-3">
              <div className="form-group">
                <label>Start Date</label>
                <input
                  type="date"
                  name="startDate"
                  className="form-control"
                  value={filters.startDate}
                  onChange={handleFilterChange}
                />
              </div>
            </div>
            <div className="col-md-3">
              <div className="form-group">
                <label>End Date</label>
                <input
                  type="date"
                  name="endDate"
                  className="form-control"
                  value={filters.endDate}
                  onChange={handleFilterChange}
                />
              </div>
            </div>
            <div className="col-md-3">
              <div className="form-group">
                <label>Min Amount</label>
                <input
                  type="number"
                  name="minAmount"
                  className="form-control"
                  value={filters.minAmount}
                  onChange={handleFilterChange}
                />
              </div>
            </div>
          </div>
          <div className="row mt-2">
            <div className="col-md-3">
              <div className="form-group">
                <label>Max Amount</label>
                <input
                  type="number"
                  name="maxAmount"
                  className="form-control"
                  value={filters.maxAmount}
                  onChange={handleFilterChange}
                />
              </div>
            </div>
            <div className="col-md-9 d-flex align-items-end">
              <button className="btn btn-primary me-2" onClick={applyFilters}>
                Apply Filters
              </button>
              <button className="btn btn-secondary" onClick={clearFilters}>
                Clear Filters
              </button>
            </div>
          </div>
        </div>
      </div>

      <table className="table table-striped">
        <thead>
          <tr>
            <th>Amount</th>
            <th>Category</th>
            <th>Description</th>
            <th>Date</th>
            <th>Type</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          {transactions?.map((transaction) => (
            <tr key={transaction.id}>
              <td>₹{transaction.amount}</td>
              <td>{transaction.category.name}</td>
              <td>{transaction.description}</td>
              <td>{new Date(transaction.date).toLocaleDateString()}</td>
              <td>
                <span
                  className={`badge ${
                    transaction.category.type === "income" ? "bg-success" : "bg-danger"
                  }`}
                >
                  {transaction.category.type}
                </span>
              </td>
              <td>
                <button
                  className="btn btn-sm btn-warning me-2"
                  onClick={() => onEdit(transaction)}
                >
                  Edit
                </button>
                <button
                  className="btn btn-sm btn-danger"
                  onClick={() => onDelete(transaction.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>

      <nav>
        <ul className="pagination">
          {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
            <li
              key={page}
              className={`page-item ${currentPage === page ? "active" : ""}`}
            >
              <button
                className="page-link"
                onClick={() => onPageChange(page, filters)}
              >
                {page}
              </button>
            </li>
          ))}
        </ul>
      </nav>
    </div>
  );
};

export default TransactionList;
