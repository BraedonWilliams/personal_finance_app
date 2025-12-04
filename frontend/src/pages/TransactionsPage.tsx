import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import type { Account, Category, Transaction } from "../types";
import {
  getTransactionsRequest,
  getAccountsRequest,
  getCategoriesRequest,
  createTransactionRequest,
  createCategoryRequest,
  type CreateTransactionPayload,
  type CreateCategoryPayload,
} from "../api/client";

const TransactionsPage: React.FC = () => {
  const { user } = useAuth();
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Form fields
  const [amount, setAmount] = useState(0);
  const [date, setDate] = useState<string>(() => {
    const today = new Date().toISOString().slice(0, 10);
    return today;
  });
  const [description, setDescription] = useState("");
  const [isIncome, setIsIncome] = useState(false);
  const [accountId, setAccountId] = useState<number | "">("");
  const [categoryId, setCategoryId] = useState<number | "">("");

  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  // Category modal
  const [showCatModal, setShowCatModal] = useState(false);
  const [newCatName, setNewCatName] = useState("");
  const [newCatType, setNewCatType] = useState<"income" | "expense">("expense");
  const [creatingCat, setCreatingCat] = useState(false);

  const loadData = async () => {
    if (!user) return;
    try {
      setLoading(true);
      setError(null);
      const [tRes, aRes, cRes] = await Promise.all([
        getTransactionsRequest(user.id, 100),
        getAccountsRequest(user.id),
        getCategoriesRequest(user.id),
      ]);
      setTransactions(tRes.data);
      setAccounts(aRes.data);
      setCategories(cRes.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load transactions/accounts/categories.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [user]);

  /* ========================
       CREATE CATEGORY
  ======================== */
  const handleCreateCategory = async () => {
    if (!user || !newCatName.trim()) return;

    try {
      setCreatingCat(true);

      const payload: CreateCategoryPayload = {
        name: newCatName,
        type: newCatType,
        user_id: user.id,
      };

      const res = await createCategoryRequest(payload);
      const created = res.data;

      // Add to list
      setCategories((prev) => [...prev, created]);

      // Auto-select it
      setCategoryId(created.id);

      // Reset modal
      setNewCatName("");
      setNewCatType("expense");
      setShowCatModal(false);
    } catch (err) {
      console.error(err);
      alert("Failed to create category.");
    } finally {
      setCreatingCat(false);
    }
  };

  /* ========================
       CREATE TRANSACTION
  ======================== */
  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || accountId === "") return;
    setSubmitError(null);
    setSubmitting(true);

    try {
      const payload: CreateTransactionPayload = {
        amount: Number(amount),
        date,
        description: description || undefined,
        is_income: isIncome,
        user_id: user.id,
        account_id: Number(accountId),
        category_id: categoryId === "" ? null : Number(categoryId),
      };

      await createTransactionRequest(payload);

      // Reset
      setAmount(0);
      setDescription("");
      setIsIncome(false);
      setCategoryId("");

      await loadData();
    } catch (err: any) {
      console.error(err);
      setSubmitError(
        err?.response?.data?.detail || "Failed to create transaction."
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (!user) return <div className="page">Please log in.</div>;

  return (
    <div className="page">
      <h1>Transactions</h1>

      {/* ===========================
              CATEGORY MODAL
      ============================ */}
      {showCatModal && (
        <div className="modal-backdrop">
          <div className="modal">
            <h3>Create Category</h3>

            <label>
              Name
              <input
                value={newCatName}
                onChange={(e) => setNewCatName(e.target.value)}
                required
              />
            </label>

            <label>
              Type
              <select
                value={newCatType}
                onChange={(e) =>
                  setNewCatType(e.target.value as "income" | "expense")
                }
              >
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </label>

            <div className="modal-actions">
              <button onClick={handleCreateCategory} disabled={creatingCat}>
                {creatingCat ? "Saving..." : "Save"}
              </button>

              <button
                onClick={() => setShowCatModal(false)}
                style={{ background: "#ccc", color: "#000" }}
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      <div className="grid-2">
        {/* LEFT COLUMN — Transactions */}
        <div className="card">
          <h2>Recent Transactions</h2>

          {loading ? (
            <p>Loading...</p>
          ) : transactions.length === 0 ? (
            <p>No transactions yet.</p>
          ) : (
            <ul>
              {transactions.map((t) => {
                const acctName =
                  accounts.find((a) => a.id === t.account_id)?.name ??
                  "Unknown account";

                const catName =
                  t.category_id == null
                    ? "Uncategorized"
                    : categories.find((c) => c.id === t.category_id)?.name ??
                      "Unknown category";

                return (
                  <li key={t.id} style={{ marginBottom: "0.25rem" }}>
                    <strong>{t.date}</strong> – {acctName} – {catName} –{" "}
                    {t.is_income ? "+" : "-"}${Number(t.amount).toFixed(2)} –{" "}
                    {t.description || "(no description)"}
                  </li>
                );
              })}
            </ul>
          )}

          {error && <div className="error">{error}</div>}
        </div>

        {/* RIGHT COLUMN — Add Transaction */}
        <div className="card">
          <h2>Add Transaction</h2>
          <form onSubmit={handleCreate} className="form">
            <label>
              Amount
              <input
                type="number"
                value={amount}
                onChange={(e) => setAmount(Number(e.target.value))}
                required
              />
            </label>

            <label>
              Date
              <input
                type="date"
                value={date}
                onChange={(e) => setDate(e.target.value)}
                required
              />
            </label>

            <label>
              Description
              <input
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </label>

            <label>
              Type
              <select
                value={isIncome ? "income" : "expense"}
                onChange={(e) => setIsIncome(e.target.value === "income")}
              >
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </label>

            <label>
              Account
              <select
                value={accountId}
                onChange={(e) =>
                  setAccountId(
                    e.target.value === "" ? "" : Number(e.target.value)
                  )
                }
                required
              >
                <option value="">Select account</option>
                {accounts.map((a) => (
                  <option key={a.id} value={a.id}>
                    {a.name} ({a.type})
                  </option>
                ))}
              </select>
            </label>

            <label>
              Category (optional)
              <select
                value={categoryId}
                onChange={(e) => {
                  if (e.target.value === "__new__") {
                    setShowCatModal(true);
                    return;
                  }
                  setCategoryId(
                    e.target.value === "" ? "" : Number(e.target.value)
                  );
                }}
              >
                <option value="">None</option>

                {categories.map((c) => (
                  <option key={c.id} value={c.id}>
                    {c.name} ({c.type})
                  </option>
                ))}

                <option value="__new__">➕ Add new category</option>
              </select>
            </label>

            {submitError && <div className="error">{submitError}</div>}

            <button type="submit" disabled={submitting}>
              {submitting ? "Adding..." : "Add Transaction"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default TransactionsPage;
