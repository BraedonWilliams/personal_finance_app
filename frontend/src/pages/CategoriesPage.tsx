import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import {
  getCategoriesRequest,
  createCategoryRequest,
  deleteCategoryRequest,
} from "../api/client";
import type { Category } from "../types";

const CategoriesPage: React.FC = () => {
  const { user } = useAuth();
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(true);

  const [name, setName] = useState("");
  const [type, setType] = useState("expense");

  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const loadCategories = async () => {
    if (!user) return;

    try {
      setLoading(true);
      const res = await getCategoriesRequest(user.id);
      setCategories(res.data);
    } catch {
      setError("Failed to load categories.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    if (user) loadCategories();
  }, [user]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;

    try {
      setSubmitting(true);
      setError(null);

      await createCategoryRequest({
        name,
        type,
        user_id: user.id,
      });

      setName("");
      setType("expense");

      await loadCategories();
    } catch (err: any) {
      setError(err?.response?.data?.detail || "Failed to create category.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDelete = async (id: number) => {
    if (!confirm("Delete this category?")) return;

    try {
      await deleteCategoryRequest(id);
      await loadCategories();
    } catch {
      alert("Failed to delete category.");
    }
  };

  if (!user) return <div className="page">Please log in.</div>;

  return (
    <div className="page">
      <h1>Categories</h1>

      <div className="grid-2">
        {/* LIST */}
        <div className="card">
          <h2>Your Categories</h2>

          {loading ? (
            <p>Loading...</p>
          ) : categories.length === 0 ? (
            <p>No categories yet.</p>
          ) : (
            <ul>
              {categories.map((c) => (
                <li
                  key={c.id}
                  style={{
                    display: "flex",
                    justifyContent: "space-between",
                    marginBottom: "0.5rem",
                  }}
                >
                  <span>
                    <strong>{c.name}</strong> ({c.type})
                  </span>
                  <button
                    style={{ color: "red" }}
                    onClick={() => handleDelete(c.id)}
                  >
                    Delete
                  </button>
                </li>
              ))}
            </ul>
          )}
        </div>

        {/* CREATE */}
        <div className="card">
          <h2>Create Category</h2>

          <form onSubmit={handleCreate} className="form">
            <label>
              Name
              <input
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </label>

            <label>
              Type
              <select value={type} onChange={(e) => setType(e.target.value)}>
                <option value="expense">Expense</option>
                <option value="income">Income</option>
              </select>
            </label>

            {error && <div className="error">{error}</div>}

            <button type="submit" disabled={submitting}>
              {submitting ? "Adding..." : "Add Category"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default CategoriesPage;
