import React, { useEffect, useMemo, useState } from "react";
import { useAuth } from "../context/AuthContext";
import type { Account, Budget, Transaction } from "../types";
import {
  getAccountsRequest,
  getBudgetsRequest,
  getTransactionsRequest,
  getDashboardSummaryRequest,
  getDashboardByCategoryRequest,
  getDashboardByMonthRequest,
  getBudgetSummaryRequest,
} from "../api/client";

import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  Legend,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";

const COLORS = [
  "#0088FE",
  "#00C49F",
  "#FFBB28",
  "#FF8042",
  "#A020F0",
  "#FF4444",
];

const DashboardPage: React.FC = () => {
  const { user } = useAuth();

  const [accounts, setAccounts] = useState<Account[]>([]);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [summary, setSummary] = useState<any>(null);
  const [categoryTotals, setCategoryTotals] = useState<any[]>([]);
  const [monthlyTotals, setMonthlyTotals] = useState<any[]>([]);
  const [budgetSummary, setBudgetSummary] = useState<any[]>([]);

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // LOAD EVERYTHING
  useEffect(() => {
    if (!user) return;

    const load = async () => {
      try {
        setLoading(true);
        setError(null);

        const [
          accRes,
          _budRes, // unused for dashboard visuals
          txRes,
          sumRes,
          catRes,
          monthRes,
          budgetSumRes,
        ] = await Promise.all([
          getAccountsRequest(user.id),
          getBudgetsRequest(user.id),
          getTransactionsRequest(user.id, 20),
          getDashboardSummaryRequest(user.id),
          getDashboardByCategoryRequest(user.id),
          getDashboardByMonthRequest(user.id),
          getBudgetSummaryRequest(user.id),
        ]);

        setAccounts(accRes.data);
        setTransactions(txRes.data);
        setSummary(sumRes.data);
        setCategoryTotals(catRes.data);
        setMonthlyTotals(monthRes.data);
        setBudgetSummary(budgetSumRes.data);
      } catch (err) {
        console.error(err);
        setError("Failed to load dashboard data.");
      } finally {
        setLoading(false);
      }
    };

    load();
  }, [user]);

  // NET WORTH
  const totalNetWorth = useMemo(
    () =>
      accounts.reduce((sum, a) => sum + (Number(a.current_balance) || 0), 0),
    [accounts]
  );

  // HIGHEST CATEGORY
  const highestCategory = useMemo(() => {
    if (!categoryTotals.length) return null;
    return categoryTotals.reduce((max, c) => (c.total > max.total ? c : max));
  }, [categoryTotals]);

  if (!user) return <div className="page">Please log in.</div>;

  return (
    <div className="page">
      <h1>Dashboard</h1>

      {loading && <p>Loading...</p>}
      {error && <div className="error">{error}</div>}

      {/* TOP CARDS */}
      <div className="grid">
        <div className="card">
          <h2>Total Net Worth</h2>
          <p style={{ fontSize: "1.5rem", fontWeight: 600 }}>
            ${totalNetWorth.toFixed(2)}
          </p>
        </div>

        <div className="card">
          <h2>Total Income (This Month)</h2>
          <p style={{ fontSize: "1.3rem", fontWeight: 600 }}>
            ${summary?.income?.toFixed(2) ?? "0.00"}
          </p>
        </div>

        <div className="card">
          <h2>Total Expenses (This Month)</h2>
          <p style={{ fontSize: "1.3rem", fontWeight: 600 }}>
            ${summary?.expenses?.toFixed(2) ?? "0.00"}
          </p>
        </div>

        <div className="card">
          <h2>Net (This Month)</h2>
          <p style={{ fontSize: "1.3rem", fontWeight: 600 }}>
            ${(summary?.income - summary?.expenses)?.toFixed(2) ?? "0.00"}
          </p>
        </div>
      </div>

      {/* CATEGORY PIE CHART */}
      <div className="grid" style={{ marginTop: "2rem" }}>
        <div className="card" style={{ textAlign: "center" }}>
          <h2>Category Breakdown</h2>
          {categoryTotals.length === 0 ? (
            <p>No data</p>
          ) : (
            <PieChart width={350} height={350}>
              <Pie
                data={categoryTotals}
                dataKey="total"
                nameKey="category"
                cx="50%"
                cy="50%"
                outerRadius={120}
                label
              >
                {categoryTotals.map((_, i) => (
                  <Cell key={i} fill={COLORS[i % COLORS.length]} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          )}
        </div>

        {/* HIGHEST CATEGORY */}
        <div className="card" style={{ textAlign: "center" }}>
          <h2>Top Category This Month</h2>
          {!highestCategory ? (
            <p>No data</p>
          ) : (
            <>
              <h3 style={{ marginTop: "1rem" }}>
                {highestCategory.category}
              </h3>
              <p style={{ fontSize: "1.5rem", fontWeight: 700 }}>
                ${highestCategory.total.toFixed(2)}
              </p>
            </>
          )}
        </div>
      </div>

      {/* MONTHLY BAR CHART */}
      <div className="card" style={{ marginTop: "2rem" }}>
        <h2>Monthly Income & Expenses</h2>
        {monthlyTotals.length === 0 ? (
          <p>No data</p>
        ) : (
          <BarChart width={600} height={300} data={monthlyTotals}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="month" />
            <YAxis />
            <Tooltip />
            <Legend />
            <Bar dataKey="expenses" fill="#FF4444" name="Expenses" />
            <Bar dataKey="income" fill="#44AAFF" name="Income" />
          </BarChart>
        )}
      </div>

      {/* ---------- BUDGET SUMMARY ---------- */}
      <div className="card" style={{ marginTop: "2rem" }}>
        <h2>Budgets</h2>

        {budgetSummary.length === 0 ? (
          <p>No budgets yet.</p>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: "1rem" }}>
            {budgetSummary.map((b: any) => {
              let color = "green";
              if (b.pct >= 100) color = "red";
              else if (b.pct >= 75) color = "orange";

              return (
                <div key={b.budget_id}>
                  {/* Title row */}
                  <div style={{ display: "flex", justifyContent: "space-between" }}>
                    <strong>{b.name}</strong>
                    <span>
                      ${b.spent.toFixed(2)} / ${b.target.toFixed(2)}
                    </span>
                  </div>

                  {/* Progress bar */}
                  <div
                    style={{
                      background: "#e5e5e5",
                      height: "10px",
                      borderRadius: "5px",
                      overflow: "hidden",
                    }}
                  >
                    <div
                      style={{
                        width: `${Math.min(b.pct, 100)}%`,
                        height: "10px",
                        background: color,
                        transition: "width 0.3s ease",
                      }}
                    />
                  </div>

                  {/* Label */}
                  <p style={{ fontSize: "0.8rem", color: color }}>
                    {b.pct >= 100
                      ? "⚠ Over budget!"
                      : b.pct >= 75
                      ? "⚠ Approaching limit..."
                      : "✓ On track"}
                  </p>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
};

export default DashboardPage;
