import React from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../../context/AuthContext";

const Navbar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login");
  };

  return (
    <nav
      style={{
        display: "flex",
        justifyContent: "space-between",
        padding: "0.75rem 1.25rem",
        backgroundColor: "#0f172a",
        color: "white",
        alignItems: "center",
      }}
    >
      <div style={{ display: "flex", gap: "1rem", alignItems: "center" }}>
        <span style={{ fontWeight: 700 }}>Personal Finance App</span>

        {user && (
          <>
            <Link to="/" style={{ color: "white", textDecoration: "none" }}>
              Dashboard
            </Link>

            <Link
              to="/accounts"
              style={{ color: "white", textDecoration: "none" }}
            >
              Accounts
            </Link>

            <Link
              to="/transactions"
              style={{ color: "white", textDecoration: "none" }}
            >
              Transactions
            </Link>

            <Link
              to="/budgets"
              style={{ color: "white", textDecoration: "none" }}
            >
              Budgets
            </Link>

            {/* ⭐ NEW CATEGORY MANAGEMENT LINK ⭐ */}
            <Link
              to="/categories"
              style={{ color: "white", textDecoration: "none" }}
            >
              Categories
            </Link>
          </>
        )}
      </div>

      <div>
        {user ? (
          <>
            <span style={{ marginRight: "1rem" }}>
              {user.username} ({user.email})
            </span>
            <button onClick={handleLogout}>Logout</button>
          </>
        ) : (
          <>
            <Link
              to="/login"
              style={{ color: "white", marginRight: "1rem" }}
            >
              Login
            </Link>
            <Link to="/signup" style={{ color: "white" }}>
              Sign Up
            </Link>
          </>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
