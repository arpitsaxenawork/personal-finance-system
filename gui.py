"""
gui.py - Modern Tkinter Desktop GUI for Personal Finance System.
Organized into 4 tabs: Dashboard, Transactions, Budgets, and Analytics/Charts.
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import datetime
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from database import DatabaseManager
from analytics import FinanceAnalytics
from visualizer import FinanceVisualizer

class FinanceAppGUI(tk.Tk):
    def __init__(self, db_path: str = "finance.db"):
        super().__init__()
        self.title("Personal Finance & Expense Analytics System")
        self.geometry("1020x680")
        self.minsize(900, 600)
        self.configure(bg="#f8fafc")

        self.db = DatabaseManager(db_path)
        self.analytics = FinanceAnalytics(self.db)
        self.visualizer = FinanceVisualizer(self.analytics)
        self.canvas = None

        self._init_styles()
        self._build_ui()
        self.refresh_data()

    def _init_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure(".", font=("Segoe UI", 9), background="#f8fafc")
        style.configure("TNotebook", background="#f8fafc", tabmargins=[4, 4, 2, 0])
        style.configure("TNotebook.Tab", font=("Segoe UI", 10, "bold"), padding=[12, 6])
        style.configure("Treeview", font=("Segoe UI", 9), rowheight=24, background="#ffffff")
        style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), background="#e2e8f0")

    def _build_ui(self):
        header = tk.Frame(self, bg="#1e293b", height=50)
        header.pack(fill="x")
        tk.Label(header, text="PERSONAL FINANCE & EXPENSE ANALYTICS SYSTEM",
                 font=("Segoe UI", 13, "bold"), fg="#f8fafc", bg="#1e293b").pack(side="left", padx=16, pady=10)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=12, pady=10)

        self.tab_dash = ttk.Frame(notebook)
        self.tab_trans = ttk.Frame(notebook)
        self.tab_budget = ttk.Frame(notebook)
        self.tab_charts = ttk.Frame(notebook)

        notebook.add(self.tab_dash, text=" 📊 Dashboard ")
        notebook.add(self.tab_trans, text=" 💳 Transactions ")
        notebook.add(self.tab_budget, text=" 🎯 Budget Planner ")
        notebook.add(self.tab_charts, text=" 📈 Analytics & Charts ")

        self._build_dashboard()
        self._build_transactions()
        self._build_budget()
        self._build_charts()

    def _build_dashboard(self):
        kpi_frame = tk.Frame(self.tab_dash, bg="#f8fafc")
        kpi_frame.pack(fill="x", padx=16, pady=16)
        self.kpi_labels = {}
        for title, key, color in [("Total Income", "income", "#10b981"), ("Total Expenses", "expense", "#ef4444"),
                                   ("Net Savings", "savings", "#0284c7"), ("Savings Rate", "rate", "#8b5cf6")]:
            card = tk.Frame(kpi_frame, bg="#ffffff", relief="ridge", bd=1, padx=14, pady=12)
            card.pack(side="left", expand=True, fill="both", padx=6)
            tk.Label(card, text=title, font=("Segoe UI", 9, "bold"), fg="#64748b", bg="#ffffff").pack(anchor="w")
            lbl = tk.Label(card, text="₹0.00", font=("Segoe UI", 14, "bold"), fg=color, bg="#ffffff")
            lbl.pack(anchor="w", pady=4)
            self.kpi_labels[key] = lbl

        tk.Label(self.tab_dash, text="Recent Transactions", font=("Segoe UI", 10, "bold"), bg="#f8fafc").pack(anchor="w", padx=20, pady=(10, 4))
        self.recent_tree = ttk.Treeview(self.tab_dash, columns=("Date", "Type", "Category", "Amount", "Desc"), show="headings", height=10)
        for col, w in [("Date", 100), ("Type", 90), ("Category", 130), ("Amount", 110), ("Desc", 250)]:
            self.recent_tree.heading(col, text=col)
            self.recent_tree.column(col, width=w, anchor="center" if col in ("Date", "Type") else "w")
        self.recent_tree.pack(fill="both", expand=True, padx=20, pady=(0, 16))

    def _build_transactions(self):
        form = tk.LabelFrame(self.tab_trans, text="Add Transaction", font=("Segoe UI", 9, "bold"), bg="#ffffff", padx=10, pady=8)
        form.pack(fill="x", padx=14, pady=8)

        self.form_date = ttk.Entry(form, width=12)
        self.form_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.form_type = ttk.Combobox(form, values=["Expense", "Income"], width=9, state="readonly")
        self.form_type.set("Expense")
        self.form_cat = ttk.Combobox(form, values=["Food", "Rent", "Travel", "Bills", "Salary", "Freelance", "Shopping", "Health"], width=13)
        self.form_cat.set("Food")
        self.form_amt = ttk.Entry(form, width=10)
        self.form_mode = ttk.Combobox(form, values=["UPI", "Cash", "Card", "Bank"], width=8, state="readonly")
        self.form_mode.set("UPI")
        self.form_desc = ttk.Entry(form, width=22)

        for col, (lbl, w) in enumerate([("Date:", self.form_date), ("Type:", self.form_type), ("Category:", self.form_cat),
                                        ("Amount (₹):", self.form_amt), ("Mode:", self.form_mode), ("Desc:", self.form_desc)]):
            tk.Label(form, text=lbl, bg="#ffffff").grid(row=0, column=col*2, padx=4, pady=4, sticky="w")
            w.grid(row=0, column=col*2+1, padx=4, pady=4)

        ttk.Button(form, text="Save Transaction", command=self._action_add_trans).grid(row=0, column=12, padx=8)

        tb = tk.Frame(self.tab_trans, bg="#f8fafc")
        tb.pack(fill="x", padx=14, pady=(2, 6))
        tk.Label(tb, text="Filter Category:", bg="#f8fafc").pack(side="left", padx=4)
        self.filter_cat = ttk.Combobox(tb, values=["All", "Food", "Rent", "Travel", "Bills", "Salary", "Freelance", "Shopping"], width=12, state="readonly")
        self.filter_cat.set("All")
        self.filter_cat.pack(side="left", padx=4)
        ttk.Button(tb, text="Filter", command=self.refresh_transactions).pack(side="left", padx=4)
        ttk.Button(tb, text="Export CSV", command=self._action_export_csv).pack(side="right", padx=4)
        ttk.Button(tb, text="Delete Selected", command=self._action_del_trans).pack(side="right", padx=4)

        self.trans_tree = ttk.Treeview(self.tab_trans, columns=("ID", "Date", "Type", "Category", "Amount", "Mode", "Desc"), show="headings")
        for col, w in [("ID", 50), ("Date", 100), ("Type", 90), ("Category", 120), ("Amount", 110), ("Mode", 90), ("Desc", 240)]:
            self.trans_tree.heading(col, text=col)
            self.trans_tree.column(col, width=w, anchor="center" if col in ("ID", "Date", "Type") else "w")
        self.trans_tree.pack(fill="both", expand=True, padx=14, pady=(0, 10))

    def _build_budget(self):
        f = tk.LabelFrame(self.tab_budget, text="Set Monthly Category Budget", font=("Segoe UI", 9, "bold"), bg="#ffffff", padx=10, pady=8)
        f.pack(fill="x", padx=14, pady=8)
        self.bg_cat = ttk.Combobox(f, values=["Food", "Rent", "Travel", "Bills", "Shopping", "Health"], width=15)
        self.bg_cat.set("Food")
        self.bg_limit = ttk.Entry(f, width=12)
        tk.Label(f, text="Category:", bg="#ffffff").grid(row=0, column=0, padx=6)
        self.bg_cat.grid(row=0, column=1, padx=6)
        tk.Label(f, text="Budget Limit (₹):", bg="#ffffff").grid(row=0, column=2, padx=6)
        self.bg_limit.grid(row=0, column=3, padx=6)
        ttk.Button(f, text="Update Budget", command=self._action_set_budget).grid(row=0, column=4, padx=10)

        self.budget_tree = ttk.Treeview(self.tab_budget, columns=("Category", "Limit", "Spent", "Variance", "Usage", "Status"), show="headings")
        for col, w in [("Category", 140), ("Limit", 120), ("Spent", 120), ("Variance", 120), ("Usage", 100), ("Status", 120)]:
            self.budget_tree.heading(col, text=col)
            self.budget_tree.column(col, width=w, anchor="center" if col in ("Usage", "Status") else "w")
        self.budget_tree.pack(fill="both", expand=True, padx=14, pady=10)

    def _build_charts(self):
        self.chart_frame = tk.Frame(self.tab_charts, bg="#ffffff", bd=1, relief="ridge")
        self.chart_frame.pack(fill="both", expand=True, padx=14, pady=10)
        self.stats_lbl = tk.Label(self.tab_charts, text="", font=("Consolas", 9), bg="#f8fafc", justify="left")
        self.stats_lbl.pack(fill="x", padx=14, pady=(0, 10))

    def refresh_data(self):
        m = self.db.get_summary_metrics()
        self.kpi_labels["income"].config(text=f"₹{m['total_income']:,.2f}")
        self.kpi_labels["expense"].config(text=f"₹{m['total_expense']:,.2f}")
        self.kpi_labels["savings"].config(text=f"₹{m['net_savings']:,.2f}")
        self.kpi_labels["rate"].config(text=f"{m['savings_rate']:.1f}%")

        self.recent_tree.delete(*self.recent_tree.get_children())
        for r in self.db.get_transactions()[:8]:
            self.recent_tree.insert("", "end", values=(r["date"], r["type"], r["category"], f"₹{r['amount']:,.2f}", r["description"]))

        self.refresh_transactions()
        self.refresh_budgets()
        self.refresh_charts()

    def refresh_transactions(self):
        self.trans_tree.delete(*self.trans_tree.get_children())
        cat = self.filter_cat.get()
        for r in self.db.get_transactions(category=cat):
            self.trans_tree.insert("", "end", values=(r["id"], r["date"], r["type"], r["category"], f"₹{r['amount']:,.2f}", r["payment_mode"], r["description"]))

    def refresh_budgets(self):
        self.budget_tree.delete(*self.budget_tree.get_children())
        for b in self.analytics.get_budget_variance():
            self.budget_tree.insert("", "end", values=(b["category"], f"₹{b['limit']:,.2f}", f"₹{b['spent']:,.2f}",
                                                       f"₹{b['variance']:,.2f}", f"{b['pct']:.1f}%", b["status"]))

    def refresh_charts(self):
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        fig = self.visualizer.create_figure()
        self.canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)

        st = self.analytics.get_expense_statistics()
        self.stats_lbl.config(text=f"NumPy Descriptive Analytics: Mean=₹{st['mean']:.2f} | Median=₹{st['median']:.2f} | Std Dev=₹{st['std']:.2f} | Min=₹{st['min']:.2f} | Max=₹{st['max']:.2f} | 75th Percentile=₹{st['q75']:.2f}")

    def _action_add_trans(self):
        try:
            amt = float(self.form_amt.get().strip())
            self.db.add_transaction(self.form_date.get().strip(), self.form_type.get(), self.form_cat.get(), amt,
                                    self.form_desc.get().strip(), self.form_mode.get())
            self.form_amt.delete(0, "end")
            self.form_desc.delete(0, "end")
            self.refresh_data()
            messagebox.showinfo("Success", "Transaction recorded successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric amount.")

    def _action_del_trans(self):
        sel = self.trans_tree.selection()
        if not sel:
            messagebox.showwarning("Warning", "Select a transaction to delete.")
            return
        trans_id = self.trans_tree.item(sel[0])["values"][0]
        if messagebox.askyesno("Confirm", f"Delete Transaction #{trans_id}?"):
            self.db.delete_transaction(trans_id)
            self.refresh_data()

    def _action_set_budget(self):
        try:
            limit = float(self.bg_limit.get().strip())
            self.db.set_budget(self.bg_cat.get().strip(), limit)
            self.bg_limit.delete(0, "end")
            self.refresh_budgets()
            messagebox.showinfo("Success", "Budget updated successfully!")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid numeric budget limit.")

    def _action_export_csv(self):
        path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if path:
            self.analytics.export_csv(path)
            messagebox.showinfo("Success", f"Data exported to {path}")
