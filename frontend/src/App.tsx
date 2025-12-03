import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Layout/Navbar";

import LoginPage from "./pages/LoginPage";
import SignupPage from "./pages/SignupPage";
import DashboardPage from "./pages/DashboardPage";
import AccountsPage from "./pages/AccountsPage";
import BudgetsPage from "./pages/BudgetsPage.tsx";
import TransactionsPage from "./pages/TransactionsPage";
import CategoriesPage from "./pages/CategoriesPage";

import { useAuth } from "./context/AuthContext";

/* // OPTIONAL: You can use this if you want per-route protection
const ProtectedRoute: React.FC<{ children: React.ReactElement }> = ({
  children,
}) => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" replace />;
  return children;
}; */

const App: React.FC = () => {
  const { user } = useAuth(); // ← FIX #1

  return (
    <div>
      <Navbar />

      <Routes>
        {/* ROOT */}
        <Route
          path="/"
          element={
            user ? <DashboardPage /> : <Navigate to="/login" replace />
          }
        />

        {/* AUTH */}
        <Route path="/login" element={<LoginPage />} />
        <Route path="/signup" element={<SignupPage />} />

        {/* PROTECTED ROUTES */}
        {user && (
          <>
            <Route path="/accounts" element={<AccountsPage />} />
            <Route path="/budgets" element={<BudgetsPage />} />
            <Route path="/transactions" element={<TransactionsPage />} />
            <Route path="/categories" element={<CategoriesPage />} /> {/* FIX #2 */}
          </>
        )}

        {/* FALLBACK */}
        <Route
          path="*"
          element={<Navigate to={user ? "/" : "/login"} replace />}
        />
      </Routes>
    </div>
  );
};

export default App;
