import React, { useEffect, useState } from 'react';
import Navbar from '../components/Navbar';
import DashboardChart from '../components/DashboardChart';
import api from '../utils/api';
import { Link } from 'react-router-dom';

const Dashboard = () => {
  const [income, setIncome] = useState(0);
  const [expenses, setExpenses] = useState(0);
  const [balance, setBalance] = useState(0);

  const fetchSummary = async () => {
    try {
      const res = await api.get('api/v1/transactions/summary/');
      setIncome(res.data.total_income);
      setExpenses(res.data.total_expense);
      setBalance(res.data.balance);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchSummary();
  }, []);

  return (
    <>
      <Navbar />
      <div className="container mt-4">
        <h2 className="mb-4">Dashboard</h2>
        <div className="row">
          <div className="col-md-4">
            <div className="card text-white bg-success mb-3">
              <div className="card-body">
                <h5 className="card-title">Total Income</h5>
                <p className="card-text">₹ {income}</p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card text-white bg-danger mb-3">
              <div className="card-body">
                <h5 className="card-title">Total Expenses</h5>
                <p className="card-text">₹ {expenses}</p>
              </div>
            </div>
          </div>
          <div className="col-md-4">
            <div className="card text-white bg-info mb-3">
              <div className="card-body">
                <h5 className="card-title">Balance</h5>
                <p className="card-text">₹ {balance}</p>
              </div>
            </div>
          </div>
        </div>

        <div className="row mt-4">
          <div className="col-md-6">
            <div className="card">
              <div className="card-header">
                <h5>Income vs Expenses</h5>
              </div>
              <div className="card-body">
                <DashboardChart income={income} expenses={expenses} />
              </div>
            </div>
          </div>
          <div className="col-md-6">
            <div className="card">
              <div className="card-header">
                <h5>Quick Actions</h5>
              </div>
              <div className="card-body">
                <div className="d-grid gap-2">
                  <Link to="/transactions" className="btn btn-primary">
                    Add New Transaction
                  </Link>
                  <Link to="/budget" className="btn btn-secondary">
                    Manage Budget
                  </Link>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default Dashboard;