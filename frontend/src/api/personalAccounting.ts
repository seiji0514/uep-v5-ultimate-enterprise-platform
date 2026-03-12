/**
 * 個人会計API（freee・マネーフォワード風）
 */
import apiClient from './client';

export interface ExpenseCategory {
  id: string;
  name: string;
  is_expense: boolean;
  note?: string;
}

export interface Expense {
  id: string;
  date: string;
  category_id: string;
  category_name: string;
  amount: number;
  description: string;
  memo?: string;
  is_expense: boolean;
  created_at: string;
}

export interface Income {
  id: string;
  date: string;
  amount: number;
  description: string;
  client_name?: string;
  memo?: string;
  created_at: string;
}

export interface DashboardSummary {
  this_month_income: number;
  this_month_expense: number;
  this_month_profit: number;
  ytd_income: number;
  ytd_expense: number;
  ytd_profit: number;
  recent_expenses: Expense[];
  recent_income: Income[];
}

export const personalAccountingApi = {
  getCategories: () =>
    apiClient.get<{ categories: ExpenseCategory[] }>('/api/v1/personal-accounting/categories').then((r) => r.data),

  suggestCategories: (q: string) =>
    apiClient.get<{ suggestions: { id: string; name: string; is_expense: boolean }[] }>(
      '/api/v1/personal-accounting/categories/suggest',
      { params: { q } }
    ).then((r) => r.data),

  getDashboard: () =>
    apiClient.get<DashboardSummary>('/api/v1/personal-accounting/dashboard').then((r) => r.data),

  getExpenses: (year?: number, month?: number) =>
    apiClient.get<{ items: Expense[]; total: number }>('/api/v1/personal-accounting/expenses', {
      params: { year, month },
    }).then((r) => r.data),

  createExpense: (data: { date: string; category_id: string; amount: number; description?: string; memo?: string }) =>
    apiClient.post<Expense>('/api/v1/personal-accounting/expenses', data).then((r) => r.data),

  deleteExpense: (id: string) =>
    apiClient.delete(`/api/v1/personal-accounting/expenses/${id}`),

  getIncome: (year?: number, month?: number) =>
    apiClient.get<{ items: Income[]; total: number }>('/api/v1/personal-accounting/income', {
      params: { year, month },
    }).then((r) => r.data),

  createIncome: (data: { date: string; amount: number; description?: string; client_name?: string; memo?: string }) =>
    apiClient.post<Income>('/api/v1/personal-accounting/income', data).then((r) => r.data),

  deleteIncome: (id: string) =>
    apiClient.delete(`/api/v1/personal-accounting/income/${id}`),

  getMonthlySummary: (year: number, month: number) =>
    apiClient.get<{ total_income: number; total_expense: number; profit: number }>(
      '/api/v1/personal-accounting/summary/monthly',
      { params: { year, month } }
    ).then((r) => r.data),
};
