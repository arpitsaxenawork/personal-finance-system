"""
analytics.py - Data Analytics & Numerical Computing Engine.
Uses Pandas and NumPy for aggregations, descriptive statistics, and budget variance.
"""
import pandas as pd
import numpy as np
from typing import Dict, Any, List
from database import DatabaseManager

class FinanceAnalytics:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def get_dataframe(self) -> pd.DataFrame:
        records = self.db.get_transactions()
        if not records:
            return pd.DataFrame(columns=["id", "date", "type", "category", "amount", "description", "payment_mode"])
        df = pd.DataFrame(records)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = pd.to_numeric(df["amount"])
        return df

    def get_expense_statistics(self) -> Dict[str, float]:
        df = self.get_dataframe()
        expenses = df[df["type"] == "Expense"]["amount"].to_numpy()
        if len(expenses) == 0:
            return {"count": 0, "mean": 0.0, "median": 0.0, "std": 0.0, "min": 0.0, "max": 0.0, "q75": 0.0}
        return {
            "count": int(len(expenses)),
            "mean": float(np.mean(expenses)),
            "median": float(np.median(expenses)),
            "std": float(np.std(expenses)),
            "min": float(np.min(expenses)),
            "max": float(np.max(expenses)),
            "q75": float(np.percentile(expenses, 75))
        }

    def get_category_breakdown(self) -> pd.Series:
        df = self.get_dataframe()
        exp_df = df[df["type"] == "Expense"]
        if exp_df.empty:
            return pd.Series(dtype=float)
        return exp_df.groupby("category")["amount"].sum().sort_values(ascending=False)

    def get_monthly_summary(self) -> pd.DataFrame:
        df = self.get_dataframe()
        if df.empty:
            return pd.DataFrame(columns=["Month", "Income", "Expense"])
        df["Month"] = df["date"].dt.strftime("%Y-%m")
        pivot = df.pivot_table(index="Month", columns="type", values="amount", aggfunc="sum", fill_value=0.0)
        for col in ["Income", "Expense"]:
            if col not in pivot.columns:
                pivot[col] = 0.0
        return pivot.reset_index()

    def get_budget_variance(self) -> List[Dict[str, Any]]:
        budgets = self.db.get_budgets()
        cat_exp = self.get_category_breakdown().to_dict()
        results = []
        for cat, limit in budgets.items():
            spent = cat_exp.get(cat, 0.0)
            variance = limit - spent
            pct = (spent / limit * 100) if limit > 0 else 0.0
            status = "Normal" if pct < 85 else ("Warning" if pct <= 100 else "Over Budget")
            results.append({"category": cat, "limit": limit, "spent": spent, "variance": variance, "pct": pct, "status": status})
        return sorted(results, key=lambda x: x["pct"], reverse=True)

    def export_csv(self, filepath: str = "transactions.csv") -> str:
        df = self.get_dataframe()
        df.to_csv(filepath, index=False)
        return filepath
