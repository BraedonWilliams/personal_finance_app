import React, { useEffect, useState } from "react";
import { useAuth } from "../context/AuthContext";
import type { Account } from "../types";
import {
  createAccountRequest,
  getAccountsRequest,
  type CreateAccountPayload,
} from "../api/client";

const AccountsPage: React.FC = () => {
  const { user } = useAuth();
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const [name, setName] = useState("");
  const [type, setType] = useState("checking");
  const [description, setDescription] = useState("");
  const [startingBalance, setStartingBalance] = useState(0);

  const [submitError, setSubmitError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  const loadAccounts = async () => {
    if (!user) return;
    try {
      setLoading(true);
      const res = await getAccountsRequest(user.id);
      setAccounts(res.data);
    } catch (err) {
      console.error(err);
      setError("Failed to load accounts.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAccounts();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!user) return;
    setSubmitError(null);
    setSubmitting(true);
    try {
      const payload: CreateAccountPayload = {
        name,
        type,
        description: description || undefined,
        starting_balance: Number(startingBalance),
        user_id: user.id,
      };
      await createAccountRequest(payload);
      setName("");
      setDescription("");
      setStartingBalance(0);
      await loadAccounts();
    } catch (err: any) {
      console.error(err);
      setSubmitError(
        err?.response?.data?.detail || "Failed to create account."
      );
    } finally {
      setSubmitting(false);
    }
  };

  if (!user) return <div className="page">Please log in.</div>;

  return (
    <div className="page">
      <h1>Accounts</h1>

      <div className="grid-2">
        <div className="card">
          <h2>Your Accounts</h2>
          {loading ? (
            <p>Loading...</p>
          ) : accounts.length === 0 ? (
            <p>No accounts yet.</p>
          ) : (
            <ul>
              {accounts.map((a) => (
                <li key={a.id}>
                  <strong>{a.name}</strong> ({a.type}) – $
                  {a.current_balance.toFixed(2)}
                </li>
              ))}
            </ul>
          )}
          {error && <div className="error">{error}</div>}
        </div>

        <div className="card">
          <h2>Create Account</h2>
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
                <option value="checking">Checking</option>
                <option value="savings">Savings</option>
                <option value="credit_card">Credit Card</option>
                <option value="investment">Investment</option>
                <option value="cash">Cash</option>
              </select>
            </label>
            <label>
              Description
              <input
                value={description}
                onChange={(e) => setDescription(e.target.value)}
              />
            </label>
            <label>
              Starting Balance
              <input
                type="number"
                value={startingBalance}
                onChange={(e) => setStartingBalance(Number(e.target.value))}
                required
              />
            </label>
            {submitError && <div className="error">{submitError}</div>}
            <button type="submit" disabled={submitting}>
              {submitting ? "Creating..." : "Create Account"}
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default AccountsPage;
