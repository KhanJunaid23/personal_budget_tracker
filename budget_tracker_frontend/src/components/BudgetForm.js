import React, { useState, useEffect } from 'react';
import api from '../utils/api';

const BudgetForm = ({ onSuccess, month, year }) => {
  const [formData, setFormData] = useState({
    amount: '',
    month: month || new Date().getMonth() + 1,
    year: year || new Date().getFullYear()
  });

  const [currentBudget, setCurrentBudget] = useState(null);

  useEffect(() => {
    const fetchBudget = async () => {
      try {
        const res = await api.get(`api/v1/budgets/?month=${formData.month}&year=${formData.year}`);
        if (res.data && res.data.length > 0) {
          setCurrentBudget(res.data[0]);
          setFormData(prev => ({ ...prev, amount: res.data[0].amount }));
        }
      } catch (err) {
        console.error(err);
      }
    };
    fetchBudget();
  }, [formData.month, formData.year]);

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = {
        amount: formData.amount,
        month: parseInt(formData.month),
        year: parseInt(formData.year)
      };

      if (currentBudget) {
        await api.put(`api/v1/budgets/${currentBudget.id}/`, data);
      } else {
        await api.post('api/v1/budgets/', data);
      }
      onSuccess();
    } catch (err) {
      console.error(err);
    }
  };

  return (
    <div className="card mb-4">
      <div className="card-header">
        <h5>{currentBudget ? 'Update' : 'Set'} Budget</h5>
      </div>
      <div className="card-body">
        <form onSubmit={handleSubmit}>
          <div className="row">
            <div className="col-md-4">
              <div className="form-group">
                <label>Month</label>
                <select
                  name="month"
                  className="form-control"
                  value={formData.month}
                  onChange={handleChange}
                  required
                >
                  {Array.from({ length: 12 }, (_, i) => i + 1).map(month => (
                    <option key={month} value={month}>
                      {new Date(2000, month - 1, 1).toLocaleString('default', { month: 'long' })}
                    </option>
                  ))}
                </select>
              </div>
            </div>
            <div className="col-md-4">
              <div className="form-group">
                <label>Year</label>
                <select
                  name="year"
                  className="form-control"
                  value={formData.year}
                  onChange={handleChange}
                  required
                >
                  {Array.from({ length: 10 }, (_, i) => new Date().getFullYear() - 5 + i).map(year => (
                    <option key={year} value={year}>{year}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="col-md-4">
              <div className="form-group">
                <label>Amount (₹)</label>
                <input
                  type="number"
                  name="amount"
                  className="form-control"
                  value={formData.amount}
                  onChange={handleChange}
                  required
                  min="0"
                  step="0.01"
                />
              </div>
            </div>
          </div>
          <button type="submit" className="btn btn-primary mt-3">
            {currentBudget ? 'Update' : 'Save'} Budget
          </button>
        </form>
      </div>
    </div>
  );
};

export default BudgetForm;