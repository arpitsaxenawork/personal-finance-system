# Personal Finance and Expense Analytics System

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Database](https://img.shields.io/badge/SQLite-ACID%20Compliant-orange.svg)](https://www.sqlite.org/)
[![Data Science](https://img.shields.io/badge/Data%20Science-NumPy%20%7C%20Pandas%20%7C%20Matplotlib-success.svg)](https://pandas.pydata.org/)
[![GUI](https://img.shields.io/badge/GUI-Tkinter%20(ttk)-informational.svg)](https://docs.python.org/3/library/tkinter.html)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

An end-to-end, lightweight desktop financial management and data intelligence application engineered in pure Python. The system provides real-time income and expense tracking, category-specific monthly budget caps with automated threshold warnings, NumPy-powered descriptive statistical analysis, and interactive Matplotlib data visualizations embedded into a modern Tkinter desktop GUI.

> **Academic Project:** Master of Computer Applications (MCA) – Data Science  
> **Institution:** Chandigarh University, Mohali, Punjab  
> **Academic Session:** 2026–2027  
> **Course:** Python Programming Lab  
> **Code Compactness:** Exactly **464 lines of modular Python code** across all files!

---

## 📌 Project Overview

Contemporary personal finance management requires disciplined expenditure monitoring to prevent discretionary deficit. Traditional manual notebooks or spreadsheets often suffer from human entry error, lack of referential constraints, and zero automated visual analytics.

The **Personal Finance and Expense Analytics System** addresses these issues through a clean **3-Tier Architecture**:
1. **Presentation Layer:** Modern Tkinter (ttk) GUI featuring an Executive Dashboard, Transaction Ledger, Budget Planner, and Embedded Matplotlib Analytics canvas, alongside an interactive terminal CLI mode.
2. **Business Logic & Analytics Layer:** NumPy for descriptive statistical distributions (Mean, Median, Standard Deviation, Quartiles) and Pandas for monthly grouping and CSV data pipelines.
3. **Data Persistence Layer:** ACID-compliant SQLite relational database (`finance.db`) executing parameterized SQL queries to prevent SQL injection vulnerabilities.

---

## ✨ Key Features

- **📊 Executive Dashboard:** Real-time KPI summary cards displaying Total Income, Total Expenses, Net Savings, and Savings Rate %, paired with recent transactions.
- **💳 Transaction Management:** Form-validated entry of daily income and expenses across standardized categories (Food, Rent, Travel, Bills, Salary, Freelance, Shopping, Health) with payment modes (UPI, Cash, Card, Bank).
- **🎯 Budget Planner & Alerts:** Category-wise monthly limits with real-time variance calculation and 3-tier status alerts (`Normal` <85%, `Warning` 85–100%, `Over Budget` >100%).
- **📈 Advanced Visual Analytics:** Dynamic Matplotlib visualizations including:
  - *Expense Distribution Donut Chart* with category percentage breakdowns.
  - *Monthly Income vs. Expense Comparison Bar Chart*.
- **📐 NumPy Descriptive Statistics:** Calculates Mean, Median, Standard Deviation, Minimum, Maximum, and 75th Percentile directly from raw transaction arrays.
- **📂 CSV Data Portability:** RFC 4180 compliant CSV export for external reporting in Excel or PowerBI.
- **⚡ Zero Setup & Offline Execution:** Self-contained relational SQLite persistence with automatic sample database seeding on first launch.

---

## 📁 Repository Structure

```text
personal_finance_system/
│
├── main.py                                      # Application entry point (CLI/GUI launcher & seed manager)
├── database.py                                  # SQLite connection manager & parameterized CRUD
├── analytics.py                                 # Pandas & NumPy statistical engine & CSV export
├── visualizer.py                                # Matplotlib chart generation & canvas rendering
├── gui.py                                       # Modern 4-tab Tkinter desktop GUI
│
├── requirements.txt                             # Python dependencies
├── .gitignore                                   # Git ignore rules
├── README.md                                    # Comprehensive project documentation
├── Personal_Finance_System_Project_Report.docx   # Academic Project Report (14 pages, formatted)
│
└── reports_and_docs/                            # Documentation, assets & chart exports
    ├── finance_dashboard_overview.png           # Exported visual analytics overview
    ├── transactions_export.csv                  # Demonstration CSV export
    └── Personal_Finance_System_Project_Report.docx
```

### Modular Codebase Line Count Summary

| Module Name | Purpose | Lines of Code |
| :--- | :--- | :---: |
| [`database.py`](database.py) | SQLite tables (`transactions`, `budgets`), CRUD, metrics | 85 |
| [`analytics.py`](analytics.py) | NumPy descriptive stats, Pandas grouping, variance | 64 |
| [`visualizer.py`](visualizer.py) | Matplotlib category donut & monthly comparison charts | 53 |
| [`gui.py`](gui.py) | Tkinter ttk 4-tab responsive desktop interface | 190 |
| [`main.py`](main.py) | CLI argument parsing, UTF-8 stdout, sample seeding | 72 |
| **Total** | **Combined across all project modules** | **464 Lines** |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher installed on your system.
- Standard libraries (`sqlite3`, `tkinter`) are pre-installed with official Python distributions.

### 1. Clone the Repository

```bash
git clone https://github.com/arpitsaxenawork/personal-finance-system.git
cd personal-finance-system
```

### 2. Install Required Packages

```bash
pip install -r requirements.txt
```

### 3. Run the Application

#### A. Launch the Desktop GUI (Default)
```bash
python main.py
```
*On first launch, the application automatically populates realistic sample transactions and budgets so you can explore the features immediately.*

#### B. Launch in Terminal / CLI Mode
```bash
python main.py --cli
```

#### C. Export High-Resolution Charts
```bash
python main.py --export
```

#### D. Re-seed Sample Database Records
```bash
python main.py --seed
```

---

## 📑 Project Report

The complete academic case study report is available in Microsoft Word format:
- 📄 **[Personal_Finance_System_Project_Report.docx](Personal_Finance_System_Project_Report.docx)** (14 pages)
  - Front page main heading: Times New Roman, 20 pt, Bold, Centered
  - Subheadings: Times New Roman, 14 pt, Bold
  - Body text: Times New Roman, 12 pt, 1.15 line spacing
  - Includes full theoretical analysis, database schema, mathematical formulations, and complete source code.

---

## 👤 Author & Academic Details

- **Student:** Arpit Saxena
- **Program:** Master of Computer Applications (MCA) – Data Science
- **Institution:** Chandigarh University, Mohali, Punjab, India
- **Academic Session:** 2026–2027

---

## 📜 License

This project is open-source and distributed under the [MIT License](LICENSE).
