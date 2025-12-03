import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import type { Budget, Category } from "../types";
import {
  getBudgetsRequest,
  getCategoriesRequest,
  createBudgetRequest,
  createCategoryRequest,
  type CreateBudgetPayload,
  type CreateCategoryPayload,
} from "../api/client";

const BudgetsPage: React.FC = () => {
  const { user } = useAuth();
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Budget form state
  const [name, setName] = useState("");
  const [targetAmount, setTargetAmount] = useState(0);
  const [period, setPeriod] = useState("monthly");
  const [categoryId, setCategoryId] = useState<number | "">("");

  const [submitting, setSubmitting] = useState(false);
  const [submitError, setSubmitError] = useState<string | null>(null);

  // Modal for creating category
  const [showCatModal, setShowCatModal] = useState(false);
  const [newCatName, setNewCatName] = useState("");
  const [newCatType, setNewCatType] = useState<"income" | "expense">("expense");
  const [creatingCat, setCreatingCat] = useState(false);

  /* ===========================
          LOAD DATA
  ============================ */
  const loadData = async () => {
    if (!user) return;

    try {
      setLoading(true);
      setError(null);

      const [bRes, cRes] = await Promise.all([
        getBudgetsRequest(user.id),
        getCategoriesRequest(user.id),
      ]);

      setBudgets(bRes.data);
      setCategories(cRes.data);
    } catch {
      setError("Failed to load budgets or categories.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) loadData();
  }, [user]);

  /* ===========================
       CREATE CATEGORY
  ============================ */
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

      // Add category locally
      setCategories((prev) => [...prev, created]);

      // Auto-select new category
      setCategoryId(created.id);

      // Reset modal
      setNewCatName("");
      setNewCatType("expense");
      setShowCatModal(false);
    } catch {
      alert("Failed to create category.");
    } finally {
      setCreatingCat(false);
    }
  };

  /* ===========================
          CREATE BUDGET
  ============================ */
  const handleCreateBudget = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user || categoryId === "") return;

    try {
      setSubmitting(true);
      setSubmitError(null);

      const payload: CreateBudgetPayload = {
        name,
        target_amount: Number(targetAmount),
        period,
        user_id: user.id,
        category_id: Number(categoryId),
      };

      await createBudgetRequest(payload);

      // Reset form
      setName("");
      setTargetAmount(0);
      setPeriod("monthly");
      setCategoryId("");

      await loadData();
    } catch (err: any) {
      setSubmitError(err?.response?.data?.detail || "Failed to create budget.");
    } finally {
      setSubmitting(false);
    }
  };

  /* ===========================
           RENDER
  ============================ */

  if (!user) return <div className="page">Please log in.</div>;

  return (
    <div className="page">
      <h1>Budgets</h1>

      {/* CATEGORY MODAL */}
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
        {/* LEFT COLUMN */}
        <div className="card">
          <h2>Your Budgets</h2>

          {loading ? (
            <p>Loading...</p>
          ) : budgets.length === 0 ? (
            <p>No budgets yet.</p>
          ) : (
            <ul>
              {budgets.map((b) => {
                const spent = b.current_spent;
                const pct = Math.min(
                  100,
                  (spent / (b.target_amount || 1)) * 100
                );
                const cat =
                  categories.find((c) => c.id === b.category_id)?.name ??
                  "Unknown";

                return (
                  <li key={b.id}>
                    <strong>{b.name}</strong> ({cat}) – $
                    {spent.toFixed(2)} / ${b.target_amount.toFixed(2)} (
                    {pct.toFixed(1)}%)
                  </li>
                );
              })}
            </ul>
          )}

          {error && <div className="error">{error}</div>}
        </div>

        {/* RIGHT COLUMN */}
        <div className="card">
          <h2>Create Budget</h2>

          <form onSubmit={handleCreateBudget} className="form">
            <label>
              Name
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </label>

            <label>
              Target Amount
              <input
                type="number"
                value={targetAmount}
                onChange={(e) => setTargetAmount(Number(e.target.value))}
                required
              />
            </label>

            <label>
              Period
              <select value={period} onChange={(e) => setPeriod(e.target.value)}>
                <option value="monthly">Monthly</option>
                <option value="weekly">Weekly</option>
                <option value="yearly">Yearly</option>
              </select>
            </label>

            <label>
              Category
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
                required
              >
                <option value="">Select category</option>

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
              {submitting ? "Creating..." : "Create Budget"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default BudgetsPage;
