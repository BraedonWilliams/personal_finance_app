import axios from "axios";

export const api = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

/* ===========================
        AUTH
=========================== */

export interface SignupPayload {
  username: string;
  email: string;
  password: string;
}

export interface LoginPayload {
  username?: string;
  email?: string;
  password: string;
}

export const signupRequest = (data: SignupPayload) =>
  api.post("/auth/signup", data);

export const loginRequest = (data: LoginPayload) =>
  api.post("/auth/login", data);

/* ===========================
       ACCOUNTS
=========================== */

export interface CreateAccountPayload {
  name: string;
  type: string;
  description?: string;
  starting_balance: number;
  user_id: number;
}

export const getAccountsRequest = (userId: number) =>
  api.get("/accounts", { params: { user_id: userId } });

export const createAccountRequest = (data: CreateAccountPayload) =>
  api.post("/accounts", data);

/* ===========================
        CATEGORIES
=========================== */

export interface CreateCategoryPayload {
  name: string;
  type: string; // "income" | "expense"
  user_id: number;
}

export const getCategoriesRequest = (userId: number) =>
  api.get(`/categories`, { params: { user_id: userId } });

export const createCategoryRequest = (payload: CreateCategoryPayload) =>
  api.post("/categories", payload);

export const deleteCategoryRequest = (categoryId: number) =>
  api.delete(`/categories/${categoryId}`);

/* ===========================
        BUDGETS
=========================== */

export interface CreateBudgetPayload {
  name: string;
  target_amount: number;
  period: string;
  user_id: number;
  category_id: number;
}

export const getBudgetsRequest = (userId: number) =>
  api.get("/budgets", { params: { user_id: userId } });

export const createBudgetRequest = (data: CreateBudgetPayload) =>
  api.post("/budgets", data);

/* ===========================
      TRANSACTIONS
=========================== */

export interface CreateTransactionPayload {
  amount: number;
  date: string;
  description?: string;
  is_income: boolean;
  user_id: number;
  account_id: number;
  category_id?: number | null;
}

export const getTransactionsRequest = (userId: number, limit = 50) =>
  api.get("/transactions", { params: { user_id: userId, limit } });

export const createTransactionRequest = (data: CreateTransactionPayload) =>
  api.post("/transactions", data);

/*
  =====================
      CHART STUFF
  =====================
*/
export const getDashboardSummaryRequest = (userId: number) =>
  api.get(`/dashboard/summary?user_id=${userId}`);

export const getDashboardByCategoryRequest = (userId: number) =>
  api.get(`/dashboard/by-category?user_id=${userId}`);

export const getDashboardByMonthRequest = (userId: number) =>
  api.get(`/dashboard/by-month?user_id=${userId}`);

export const getBudgetSummaryRequest = (userId: number) =>
  api.get(`/dashboard/budget-summary`, {
    params: { user_id: userId },
  });


