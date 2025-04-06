import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import BudgetForm from '../components/BudgetForm';
import BudgetChart from '../components/BudgetChart';
import api from '../utils/api';

const Budget = () => {
  const [budgetData, setBudgetData] = useState({
    budget: 0,
    actual_expense: 0,
    remaining: 0
  });
  const [selectedMonth, setSelectedMonth] = useState(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState(new Date().getFullYear());

  const fetchBudgetData = async (month, year) => {
    try {
      const res = await api.get(`api/v1/budgets/summary/?month=${month}&year=${year}`);
      setBudgetData({
        budget: res.data.budget,
        actual_expense: res.data.actual_expense,
        remaining: res.data.remaining
      });
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchBudgetData(selectedMonth, selectedYear);
  }, [selectedMonth, selectedYear]);

  const handleMonthYearChange = (month, year) => {
    setSelectedMonth(month);
    setSelectedYear(year);
  };

  const handleSuccess = () => {
    fetchBudgetData(selectedMonth, selectedYear);
  };

  return (
    <>
      <Navbar />
      <div className="container mt-4">
        <h2 className="mb-4">Budget Management</h2>
        
        <BudgetForm 
          onSuccess={handleSuccess} 
          month={selectedMonth} 
          year={selectedYear}
          onMonthYearChange={handleMonthYearChange}
        />

        <div className="row">
          <div className="col-md-6">
            <div className="card mb-4">
              <div className="card-header">
                <h5>Budget Overview</h5>
              </div>
              <div className="card-body">
                <div className="row">
                  <div className="col-md-4">
                    <div className="card bg-primary text-white mb-3">
                      <div className="card-body">
                        <h6 className="card-title">Budget</h6>
                        <h4>₹{budgetData.budget.toLocaleString()}</h4>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-4">
                    <div className="card bg-danger text-white mb-3">
                      <div className="card-body">
                        <h6 className="card-title">Expenses</h6>
                        <h4>₹{budgetData.actual_expense.toLocaleString()}</h4>
                      </div>
                    </div>
                  </div>
                  <div className="col-md-4">
                    <div className={`card ${budgetData.remaining >= 0 ? 'bg-success' : 'bg-warning'} text-white mb-3`}>
                      <div className="card-body">
                        <h6 className="card-title">Remaining</h6>
                        <h4>₹{budgetData.remaining.toLocaleString()}</h4>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div className="card mb-4">
              <div className="card-header">
                <h5>Budget vs Expenses</h5>
              </div>
              <div className="card-body">
                <BudgetChart 
                  budget={budgetData.budget} 
                  expenses={budgetData.actual_expense} 
                />
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Budget;