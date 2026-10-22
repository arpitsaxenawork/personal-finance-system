"""
visualizer.py - Matplotlib Data Visualizations for Personal Finance System.
Generates publication-quality charts for desktop GUI and reports.
"""
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import os
from analytics import FinanceAnalytics

class FinanceVisualizer:
    def __init__(self, analytics: FinanceAnalytics):
        self.analytics = analytics
        self.palette = ["#0284c7", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6", "#ec4899", "#14b8a6"]

    def create_figure(self) -> Figure:
        fig = Figure(figsize=(9.5, 4.2), dpi=100)
        fig.patch.set_facecolor("#ffffff")
        ax1, ax2 = fig.subplots(1, 2)

        # Plot 1: Category Expense Donut Chart
        breakdown = self.analytics.get_category_breakdown()
        if not breakdown.empty:
            wedges, texts, autotexts = ax1.pie(
                breakdown.values, labels=breakdown.index, autopct="%1.1f%%",
                startangle=140, colors=self.palette[:len(breakdown)],
                wedgeprops=dict(width=0.45, edgecolor="white", linewidth=2)
            )
            for at in autotexts:
                at.set_fontsize(8)
                at.set_weight("bold")
            ax1.set_title("Expense by Category", fontsize=11, fontweight="bold", pad=10)
        else:
            ax1.text(0.5, 0.5, "No Expense Data", ha="center", va="center", color="#64748b")
            ax1.axis("off")

        # Plot 2: Monthly Income vs Expense
        monthly = self.analytics.get_monthly_summary()
        if not monthly.empty:
            x = range(len(monthly))
            width = 0.35
            ax2.bar([i - width/2 for i in x], monthly["Income"], width, label="Income", color="#10b981")
            ax2.bar([i + width/2 for i in x], monthly["Expense"], width, label="Expense", color="#ef4444")
            ax2.set_xticks(list(x))
            ax2.set_xticklabels(monthly["Month"], rotation=15, fontsize=8)
            ax2.set_title("Monthly Income vs Expense", fontsize=11, fontweight="bold", pad=10)
            ax2.legend(fontsize=8)
            ax2.grid(axis="y", linestyle="--", alpha=0.3)
        else:
            ax2.text(0.5, 0.5, "No Monthly Data", ha="center", va="center", color="#64748b")
            ax2.axis("off")

        fig.tight_layout()
        return fig

    def save_charts(self, filepath: str = "reports_and_docs/finance_dashboard_overview.png") -> str:
        os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
        fig = self.create_figure()
        fig.savefig(filepath, dpi=200, bbox_inches="tight")
        return filepath
