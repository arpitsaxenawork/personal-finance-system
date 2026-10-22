"""
main.py - Application Launcher & Seed Manager for Personal Finance System.
Supports GUI launch, interactive CLI mode, and CSV/chart exports.
"""
import sys
import argparse
import os

if sys.platform.startswith("win") and hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
from database import DatabaseManager
from analytics import FinanceAnalytics
from visualizer import FinanceVisualizer

def seed_sample_data(db: DatabaseManager):
    """Seed realistic monthly financial records for demonstration."""
    if len(db.get_transactions()) > 0:
        return
    samples = [
        ("2026-10-01", "Income", "Salary", 65000.0, "Monthly Corporate Salary", "Bank"),
        ("2026-10-02", "Expense", "Rent", 16000.0, "Apartment Monthly Rent", "Bank"),
        ("2026-10-04", "Expense", "Food", 3450.0, "Supermarket Grocery Shopping", "Card"),
        ("2026-10-05", "Expense", "Bills", 2200.0, "Electricity and Water Bill", "UPI"),
        ("2026-10-08", "Expense", "Travel", 1850.0, "Metro Pass and Fuel Refill", "UPI"),
        ("2026-10-10", "Income", "Freelance", 12500.0, "Web Consulting Project", "Bank"),
        ("2026-10-12", "Expense", "Food", 1850.0, "Weekend Dining Out", "UPI"),
        ("2026-10-15", "Expense", "Shopping", 4200.0, "Winter Apparel Purchase", "Card"),
        ("2026-10-18", "Expense", "Bills", 999.0, "Broadband Internet Plan", "UPI"),
        ("2026-10-20", "Expense", "Health", 1250.0, "Pharmacy Medicines", "UPI"),
        ("2026-10-22", "Expense", "Food", 1450.0, "Weekly Fresh Vegetables", "Cash")
    ]
    for d, t, c, a, desc, m in samples:
        db.add_transaction(d, t, c, a, desc, m)
    for cat, lim in [("Food", 8000), ("Rent", 17000), ("Bills", 4000), ("Travel", 3000), ("Shopping", 5000)]:
        db.set_budget(cat, lim)

def run_cli(db: DatabaseManager):
    analytics = FinanceAnalytics(db)
    m = db.get_summary_metrics()
    print("=" * 60)
    print("PERSONAL FINANCE & EXPENSE ANALYTICS SYSTEM (CLI)")
    print("=" * 60)
    print(f"Total Income:     ₹{m['total_income']:,.2f}")
    print(f"Total Expenses:   ₹{m['total_expense']:,.2f}")
    print(f"Net Savings:      ₹{m['net_savings']:,.2f} ({m['savings_rate']:.1f}%)")
    print("-" * 60)
    print("Descriptive Analytics (NumPy):")
    st = analytics.get_expense_statistics()
    print(f"Mean: ₹{st['mean']:.2f} | Median: ₹{st['median']:.2f} | Std: ₹{st['std']:.2f} | Max: ₹{st['max']:.2f}")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Personal Finance System")
    parser.add_argument("--cli", action="store_true", help="Run interactive CLI mode")
    parser.add_argument("--seed", action="store_true", help="Re-seed sample transactions")
    parser.add_argument("--export", action="store_true", help="Export summary charts to PNG")
    args = parser.parse_args()

    db = DatabaseManager("finance.db")
    seed_sample_data(db)

    if args.seed:
        print("[+] Database seeded with demonstration records.")
    elif args.export:
        vis = FinanceVisualizer(FinanceAnalytics(db))
        out = vis.save_charts("reports_and_docs/finance_dashboard_overview.png")
        print(f"[+] Dashboard charts exported to: {out}")
    elif args.cli:
        run_cli(db)
    else:
        from gui import FinanceAppGUI
        app = FinanceAppGUI("finance.db")
        app.mainloop()

if __name__ == "__main__":
    main()
