"""
database.py - SQLite Database Management for Personal Finance System.
Handles schema creation, parameterized CRUD operations, and budget tracking.
"""
import sqlite3
from typing import List, Dict, Any, Optional

class DatabaseManager:
    def __init__(self, db_path: str = "finance.db"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        with self._get_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS transactions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date TEXT NOT NULL,
                    type TEXT NOT NULL CHECK(type IN ('Income', 'Expense')),
                    category TEXT NOT NULL,
                    amount REAL NOT NULL CHECK(amount > 0),
                    description TEXT,
                    payment_mode TEXT DEFAULT 'UPI'
                );
                CREATE TABLE IF NOT EXISTS budgets (
                    category TEXT PRIMARY KEY,
                    monthly_limit REAL NOT NULL CHECK(monthly_limit > 0)
                );
            """)

    def add_transaction(self, date: str, trans_type: str, category: str, amount: float,
                        description: str = "", payment_mode: str = "UPI") -> int:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO transactions (date, type, category, amount, description, payment_mode)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (date, trans_type.capitalize(), category.strip(), float(amount), description.strip(), payment_mode))
            return cur.lastrowid

    def delete_transaction(self, trans_id: int) -> bool:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM transactions WHERE id = ?", (trans_id,))
            return cur.rowcount > 0

    def get_transactions(self, category: Optional[str] = None, trans_type: Optional[str] = None,
                         keyword: Optional[str] = None) -> List[Dict[str, Any]]:
        query = "SELECT * FROM transactions WHERE 1=1"
        params = []
        if category and category != "All":
            query += " AND category = ?"
            params.append(category)
        if trans_type and trans_type != "All":
            query += " AND type = ?"
            params.append(trans_type.capitalize())
        if keyword:
            query += " AND (description LIKE ? OR category LIKE ?)"
            params.extend([f"%{keyword}%", f"%{keyword}%"])
        query += " ORDER BY date DESC, id DESC"
        with self._get_connection() as conn:
            return [dict(row) for row in conn.cursor().execute(query, params).fetchall()]

    def set_budget(self, category: str, limit: float):
        with self._get_connection() as conn:
            conn.cursor().execute("""
                INSERT INTO budgets (category, monthly_limit) VALUES (?, ?)
                ON CONFLICT(category) DO UPDATE SET monthly_limit = excluded.monthly_limit
            """, (category.strip(), float(limit)))

    def get_budgets(self) -> Dict[str, float]:
        with self._get_connection() as conn:
            cur = conn.cursor().execute("SELECT category, monthly_limit FROM budgets")
            return {row["category"]: row["monthly_limit"] for row in cur.fetchall()}

    def get_summary_metrics(self) -> Dict[str, float]:
        with self._get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN type = 'Income' THEN amount ELSE 0 END), 0) AS income,
                    COALESCE(SUM(CASE WHEN type = 'Expense' THEN amount ELSE 0 END), 0) AS expense
                FROM transactions
            """)
            row = cur.fetchone()
            inc, exp = row["income"], row["expense"]
            savings = inc - exp
            rate = (savings / inc * 100) if inc > 0 else 0.0
            return {"total_income": inc, "total_expense": exp, "net_savings": savings, "savings_rate": rate}
