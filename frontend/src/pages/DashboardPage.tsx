import React, { useEffect, useMemo, useState } from "react";
import { useAuth } from "../context/AuthContext";
import type { Account, Budget, Transaction } from "../types";
import {
  getAccountsRequest,
  getBudgetsRequest,
  getTransactionsRequest,
} from "../api/client";

const DashboardPage: React.FC = () => {
  const { user } = useAuth();
  const [accounts, setAccounts] = useState<Account[]>([]);
  const [budgets, setBudgets] = useState<Budget[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!user) return;

    const load = async () => {
      try {
        setLoading(true);
        setError(null);

        const [accRes, budRes, txRes] = await Promise.all([
          getAccountsRequest(user.id),
          getBudgetsRequest(user.id),
          getTransactionsRequest(user.id, 10),
        ]);

        setAccounts(accRes.data);
        setBudgets(budRes.data);
        setTransactions(txRes.data);
      } catch (err: any) {
        console.error(err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [user]);

  const totalNetWorth = useMemo(
    () => accounts.reduce((sum, a) => sum + (a.current_balance ?? 0), 0),
    [accounts]
  );

  if (!user) return <div className="page">Please log in.</div>;

  return (
    <div className="page">
      <h1>Dashboard</h1>
      {loading && <p>Loading...</p>}
      {error && <div className="error">{error}</div>}

      <div className="grid">
        <div className="card">
          <h2>Total Net Worth</h2>
          <p style={{ fontSize: "1.5rem", fontWeight: 600 }}>
            ${totalNetWorth.toFixed(2)}
          </p>
        </div>

        <div className="card">
          <h2>Accounts</h2>
          {accounts.length === 0 ? (
            <p>No accounts yet.</p>
          ) : (
            <ul>
              {accounts.map((a) => (
                <li key={a.id}>
                  {a.name} – ${a.current_balance.toFixed(2)} ({a.type})
                </li>
              ))}
            </ul>
          )}
        </div>

        <div className="card">
          <h2>Budgets</h2>
          {budgets.length === 0 ? (
            <p>No budgets yet.</p>
          ) : (
            <ul>
              {budgets.map((b) => {
                const used = b.current_spent;
                const pct = Math.min(
                  100,
                  (used / (b.target_amount || 1)) * 100
                );
                return (
                  <li key={b.id} style={{ marginBottom: "0.5rem" }}>
                    <strong>{b.name}</strong> – ${used.toFixed(2)} / $
                    {b.target_amount.toFixed(2)} ({pct.toFixed(1)}%)
                  </li>
                );
              })}
            </ul>
          )}
        </div>

        <div className="card">
          <h2>Recent Transactions</h2>
          {transactions.length === 0 ? (
            <p>No transactions yet.</p>
          ) : (
            <ul>
              {transactions.map((t) => (
                <li key={t.id}>
                  {t.date} – {t.description || "(no description)"} –{" "}
                  {t.is_income ? "+" : "-"}${Number(t.amount).toFixed(2)}
                </li>
              ))}
            </ul>
          )}
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;
