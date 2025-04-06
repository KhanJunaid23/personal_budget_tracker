import React, { useState, useEffect } from 'react';
import Navbar from '../components/Navbar';
import TransactionForm from '../components/TransactionForm';
import TransactionList from '../components/TransactionList';
import api from '../utils/api';

const Transactions = () => {
  const [transactions, setTransactions] = useState([]);
  const [editingTransaction, setEditingTransaction] = useState(null);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [showForm, setShowForm] = useState(false);

  const fetchTransactions = async (page = 1, filters = {}) => {
    try {
      const params = new URLSearchParams({page,...filters}).toString();
      const res = await api.get(`api/v1/transactions/?${params}`);
      setTransactions(res.data);
      setTotalPages(Math.ceil(res.data.count / 10));
      setCurrentPage(page);
    } catch (err) {
      console.error(err);
    }
  };

  useEffect(() => {
    fetchTransactions();
  }, []);

  const handleDelete = async (id) => {
    try {
      await api.delete(`api/v1/transactions/${id}/`);
      fetchTransactions(currentPage);
    } catch (err) {
      console.error(err);
    }
  };

  const handleSuccess = () => {
    setShowForm(false);
    setEditingTransaction(null);
    fetchTransactions(currentPage);
  };

  return (
    <>
      <Navbar />
      <div className="container mt-4">
        <div className="d-flex justify-content-between align-items-center mb-4">
          <h2>Transactions</h2>
          <button
            className="btn btn-primary"
            onClick={() => {
              setEditingTransaction(null);
              setShowForm(true);
            }}
          >
            Add Transaction
          </button>
        </div>

        {showForm && (
          <TransactionForm
            transaction={editingTransaction}
            onSuccess={handleSuccess}
          />
        )}

        <TransactionList
          transactions={transactions}
          onEdit={(transaction) => {
            setEditingTransaction(transaction);
            setShowForm(true);
          }}
          onDelete={handleDelete}
          onPageChange={fetchTransactions}
          currentPage={currentPage}
          totalPages={totalPages}
        />
      </div>
    </>
  );
};

export default Transactions;