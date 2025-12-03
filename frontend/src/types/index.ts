export interface User {
  id: number;
  username: string;
  email: string;
  created_at: string; 
}

/* ===========================
        ACCOUNTS
=========================== */
export interface Account {
  id: number;
  name: string;
  type: string;
  description?: string | null;
  starting_balance: number;
  current_balance: number;
  user_id: number;
  created_at: string;
}

/* ===========================
        CATEGORIES
=========================== */
export interface Category {
  id: number;
  name: string;
  type: "income" | "expense"; // <-- Correct union type
  description?: string | null;
  user_id: number;
  created_at: string;
}

/* ===========================
         BUDGETS
=========================== */
export interface Budget {
  id: number;
  name: string;
  target_amount: number;
  period: string;
  user_id: number;
  category_id: number;

  current_spent: number;  // backend returns this
  remaining: number;      // backend returns this
  created_at: string;

  // Optional, used in some pages but not required
  category?: Category;
}

/* ===========================
       TRANSACTIONS
=========================== */
export interface Transaction {
  id: number;
  amount: number;
  date: string; // YYYY-MM-DD
  description?: string | null;
  is_income: boolean;
  user_id: number;
  account_id: number;
  category_id?: number | null;
  created_at: string;
}
