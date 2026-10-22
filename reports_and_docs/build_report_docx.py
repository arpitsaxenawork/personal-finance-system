"""
build_report_docx.py
Generates the comprehensive academic report in .docx format.
Adheres strictly to formatting guidelines:
- Front Page Main Heading: Times New Roman, 20 pt, Bold, Center
- Subheadings: Times New Roman, 14 pt, Bold
- Body Paragraphs: Times New Roman, 12 pt, 1.15 line spacing
- Complete Python source code included (~464 lines)
- Total length: exactly 10 to 14 pages (target: 12-13 pages in Word)
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=60, bottom=60, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, color="CBD5E1", sz="4", val="single"):
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

def add_body_p(doc, text, bold_prefix=None, space_after=3):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)  # Strict requirement: 12 pt body
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_bullet_p(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Times New Roman"
        r_pre.font.size = Pt(12)
        r_pre.font.bold = True
        r_pre.font.color.rgb = RGBColor(15, 23, 42)
    r = p.add_run(text)
    r.font.name = "Times New Roman"
    r.font.size = Pt(12)  # Strict requirement: 12 pt body
    r.font.color.rgb = RGBColor(30, 41, 59)
    return p

def add_subheading(doc, text, level=1, space_before=6):
    p = doc.add_paragraph()
    p.paragraph_format.keep_with_next = True
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(2)
    run = p.add_run(text)
    run.font.name = "Times New Roman"
    run.font.size = Pt(14)  # Strict requirement: 14 for subheadings
    run.font.bold = True
    if level == 1:
        run.font.color.rgb = RGBColor(27, 54, 93)
    else:
        run.font.color.rgb = RGBColor(30, 64, 110)
    return p

def add_code_block(doc, file_name, code_text):
    add_subheading(doc, f"Module Source Code: {file_name}", level=2, space_before=4)
    
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    
    cell = table.cell(0, 0)
    cell.width = Inches(6.8)
    set_cell_background(cell, "F8FAFC")
    set_cell_borders(cell, color="CBD5E1", sz="4", val="single")
    set_cell_margins(cell, top=40, bottom=40, left=80, right=80)
    
    lines = code_text.strip().split("\n")
    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = Pt(9.5)  # Crisp compact line spacing for code
    
    for idx, line in enumerate(lines):
        if idx > 0:
            p = cell.add_paragraph()
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = Pt(9.5)
        run = p.add_run(line)
        run.font.name = "Consolas"
        run.font.size = Pt(8.0)
        run.font.color.rgb = RGBColor(30, 41, 59)
        
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def generate_report():
    doc = docx.Document()
    
    for s in doc.sections:
        s.top_margin = Inches(0.85)
        s.bottom_margin = Inches(0.85)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)

    # -------------------------------------------------------------
    # PAGE 1: TITLE / FRONT PAGE
    # -------------------------------------------------------------
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(28)
    p_inst.paragraph_format.space_after = Pt(4)
    r_inst = p_inst.add_run("CHANDIGARH UNIVERSITY")
    r_inst.font.name = "Times New Roman"
    r_inst.font.size = Pt(16)
    r_inst.font.bold = True
    r_inst.font.color.rgb = RGBColor(27, 54, 93)

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(4)
    r_dept = p_dept.add_run("University Institute of Computing (UIC)\nDepartment of Computer Applications")
    r_dept.font.name = "Times New Roman"
    r_dept.font.size = Pt(13)
    r_dept.font.color.rgb = RGBColor(71, 85, 105)

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(10)
    p_div.paragraph_format.space_after = Pt(20)
    r_div = p_div.add_run("―" * 42)
    r_div.font.color.rgb = RGBColor(203, 213, 225)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(10)
    r_sub = p_sub.add_run("PYTHON PROGRAMMING MINI-PROJECT REPORT")
    r_sub.font.name = "Times New Roman"
    r_sub.font.size = Pt(14)
    r_sub.font.bold = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    # REQUIREMENT: Times New Roman 20 for main heading in front page
    p_main = doc.add_paragraph()
    p_main.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_main.paragraph_format.space_before = Pt(14)
    p_main.paragraph_format.space_after = Pt(14)
    r_main = p_main.add_run("PERSONAL FINANCE AND EXPENSE ANALYTICS SYSTEM")
    r_main.font.name = "Times New Roman"
    r_main.font.size = Pt(20)  # STRICT REQUIREMENT
    r_main.font.bold = True
    r_main.font.color.rgb = RGBColor(27, 54, 93)

    p_desc = doc.add_paragraph()
    p_desc.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_desc.paragraph_format.space_after = Pt(36)
    r_desc = p_desc.add_run("An End-to-End Financial Intelligence Solution Built with SQLite, NumPy, Pandas, Matplotlib, and Modern Tkinter GUI")
    r_desc.font.name = "Times New Roman"
    r_desc.font.size = Pt(12)
    r_desc.font.italic = True
    r_desc.font.color.rgb = RGBColor(71, 85, 105)

    # Submission Box
    tbl = doc.add_table(rows=2, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    
    cell_lh = tbl.cell(0, 0)
    cell_rh = tbl.cell(0, 1)
    cell_lb = tbl.cell(1, 0)
    cell_rb = tbl.cell(1, 1)
    
    w_box = Inches(3.3)
    cell_lh.width, cell_rh.width, cell_lb.width, cell_rb.width = w_box, w_box, w_box, w_box
    
    p = cell_lh.paragraphs[0]
    r = p.add_run("SUBMITTED BY:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    p = cell_rh.paragraphs[0]
    r = p.add_run("SUBMITTED TO:")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = RGBColor(27, 54, 93)
    
    p = cell_lb.paragraphs[0]
    r = p.add_run("Name: Arpit Saxena\nCourse: MCA (Data Science)\nSemester: 1st Semester\nAcademic Session: 2026–2027")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 41, 59)
    
    p = cell_rb.paragraphs[0]
    r = p.add_run("Department of Computer Applications\nUniversity Institute of Computing\nChandigarh University, Mohali\nPunjab - 140413")
    r.font.name = "Times New Roman"
    r.font.size = Pt(11)
    r.font.color.rgb = RGBColor(30, 41, 59)

    for r_idx in range(2):
        for c_idx in range(2):
            cell = tbl.cell(r_idx, c_idx)
            set_cell_background(cell, "F8FAFC")
            set_cell_borders(cell, color="CBD5E1", sz="4", val="single")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    doc.add_page_break()  # End Page 1

    # -------------------------------------------------------------
    # PAGE 2: CERTIFICATE OF ORIGINALITY & TABLE OF CONTENTS
    # -------------------------------------------------------------
    add_subheading(doc, "CERTIFICATE OF ORIGINAL WORK", level=1)
    add_body_p(doc, "This is to certify that the project entitled 'Personal Finance and Expense Analytics System' submitted by Arpit Saxena (MCA Data Science, 1st Semester) to Chandigarh University, Mohali, is a bonafide record of original academic work carried out under faculty guidance in partial fulfillment of the requirements for the Master of Computer Applications (MCA) Degree in Python Programming Lab.")
    add_body_p(doc, "The code, database structures, analytical algorithms, and user interface presented in this report have been developed independently, strictly adhering to academic integrity standards and Python engineering best practices.")

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(16)
    p_sig.paragraph_format.space_after = Pt(14)
    r_sig = p_sig.add_run("Faculty Guide / Project Evaluator                                Student Candidate\nDepartment of Computer Applications                           Arpit Saxena (MCA)")
    r_sig.font.name = "Times New Roman"
    r_sig.font.size = Pt(11)
    r_sig.font.bold = True
    r_sig.font.color.rgb = RGBColor(71, 85, 105)

    add_subheading(doc, "TABLE OF CONTENTS", level=1)
    toc_items = [
        ("1. Abstract & Introduction", "3"),
        ("2. Problem Statement, Aim & Comparative Analysis", "3"),
        ("3. System Architecture & Relational Database Design", "4"),
        ("4. Mathematical Methodology & Analytical Formulations", "4"),
        ("5. Graphical User Interface & Visual Output Screens", "5"),
        ("6. Conclusion, Academic Learning & Future Scope", "5"),
        ("7. Complete Source Code Implementation", "6"),
        ("   7.1 Database Manager Module (database.py)", "6"),
        ("   7.2 Data Analytics & Numerical Engine (analytics.py)", "7"),
        ("   7.3 Data Visualization Module (visualizer.py)", "8"),
        ("   7.4 Desktop User Interface Module (gui.py)", "9"),
        ("   7.5 Application Launcher & Seed Manager (main.py)", "11"),
    ]
    for title, page_no in toc_items:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(0)
        p_toc.paragraph_format.space_after = Pt(2)
        r_t = p_toc.add_run(title)
        r_t.font.name = "Times New Roman"
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = RGBColor(30, 41, 59)
        if not title.startswith("   "):
            r_t.font.bold = True
        
        dots_count = max(4, 75 - len(title))
        r_dots = p_toc.add_run(" " + "." * dots_count + " ")
        r_dots.font.name = "Times New Roman"
        r_dots.font.size = Pt(10)
        r_dots.font.color.rgb = RGBColor(148, 163, 184)
        
        r_p = p_toc.add_run(page_no)
        r_p.font.name = "Times New Roman"
        r_p.font.size = Pt(11)
        r_p.font.bold = True
        r_p.font.color.rgb = RGBColor(27, 54, 93)

    doc.add_page_break()  # End Page 2

    # -------------------------------------------------------------
    # PAGE 3: ABSTRACT, INTRODUCTION & PROBLEM STATEMENT
    # -------------------------------------------------------------
    add_subheading(doc, "1. ABSTRACT & INTRODUCTION", level=1)
    add_subheading(doc, "1.1 Abstract", level=2)
    add_body_p(doc, "In contemporary individual economics, systematic financial management and disciplined expenditure tracking are foundational to achieving financial solvency, wealth preservation, and long-term investment goals. Conventional manual bookkeeping techniques—including paper ledgers, fragmented payment receipts, and unstandardized spreadsheets—frequently suffer from human arithmetic discrepancies, accidental record omission, lack of relational referential integrity, and an absence of automated visual intelligence.")
    add_body_p(doc, "This mini-project presents the Personal Finance and Expense Analytics System, an end-to-end Python desktop application engineered to streamline daily transaction recording, budgetary accountability, and multi-dimensional financial analytics. Developed with Python 3.13, the solution integrates an ACID-compliant SQLite relational database for robust offline persistence, Pandas and NumPy for vectorized statistical calculations (mean, median, standard deviation, quartiles, and pivot aggregations), Matplotlib for publication-grade visualization canvases, and a modern Tkinter (ttk) graphical user interface. The entire software implementation is compactly structured in approximately 464 lines of modular Python code, balancing elegance, computational rigor, and strict academic standards.")

    add_subheading(doc, "1.2 Introduction & Background", level=2)
    add_body_p(doc, "The rapid proliferation of cashless transactions via Unified Payments Interface (UPI), contactless credit cards, and digital wallets has exponentially increased daily micro-transactions. Without structured monitoring, discretionary expenditures frequently exceed budgeted limits. Python delivers an ideal foundation for data-centric software through clean syntax, rich standard modules, and robust scientific packages. Designed as a 3-tier desktop architecture, the application empowers users to record daily income and expenses across standardized categories, maintain category spending caps with variance alerts, compute rigorous descriptive statistics, export data to CSV, and visualize spending habits through interactive charts.")

    add_subheading(doc, "2. PROBLEM STATEMENT & OBJECTIVES", level=1)
    add_body_p(doc, "Consumers face fragmented records across UPI and cards, lack proactive warnings for overspending, and miss cognitive insights from raw numerical totals. This project aims to deliver a standalone, secure, offline desktop analytics tool that guarantees ACID persistence, enforces OOP data validation, computes NumPy descriptive statistics, produces dynamic Matplotlib charts, and provides RFC 4180 CSV export.")

    doc.add_page_break()  # End Page 3

    # -------------------------------------------------------------
    # PAGE 4: COMPARATIVE ANALYSIS, ARCHITECTURE & SCHEMA
    # -------------------------------------------------------------
    add_subheading(doc, "2.1 Comparative Analysis: Existing vs. Proposed System", level=2)
    comp_tbl = doc.add_table(rows=5, cols=3)
    comp_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    comp_tbl.autofit = False
    headers = ["Evaluation Metric", "Manual Ledgers / Excel", "Proposed Personal Finance System"]
    widths = [Inches(1.8), Inches(2.3), Inches(2.6)]
    
    for c_idx, h_text in enumerate(headers):
        cell = comp_tbl.cell(0, c_idx)
        cell.width = widths[c_idx]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    comp_data = [
        ("Data Entry & Validation", "Manual entry prone to typos and type mismatches", "Strict form-validated GUI inputs enforcing positive values"),
        ("Storage & Persistence", "Prone to workbook corruption and accidental deletion", "ACID-compliant SQLite relational database with rollback"),
        ("Budget Monitoring", "Manual month-end reconciliation formula writing", "Real-time automated variance calculation & color threshold alerts"),
        ("Visual & Statistical Engine", "Static, manual chart construction", "Automated NumPy statistical metrics & dynamic Matplotlib charts")
    ]
    for r_idx, row in enumerate(comp_data, start=1):
        for c_idx, val in enumerate(row):
            cell = comp_tbl.cell(r_idx, c_idx)
            cell.width = widths[c_idx]
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_borders(cell, color="CBD5E1", sz="4", val="single")
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(9)
            r.font.color.rgb = RGBColor(30, 41, 59)

    add_subheading(doc, "3. SYSTEM ARCHITECTURE & DATABASE DESIGN", level=1)
    add_body_p(doc, "The software follows a 3-tier desktop architectural pattern: (1) Presentation Tier (Tkinter GUI in gui.py & CLI in main.py); (2) Business Logic Tier (Pandas grouping, NumPy statistics in analytics.py, and Matplotlib chart generation in visualizer.py); (3) Data Persistence Tier (SQLite relational database manager in database.py).")

    add_subheading(doc, "3.1 Relational Database Schema", level=2)
    schema_tbl = doc.add_table(rows=8, cols=4)
    schema_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    schema_tbl.autofit = False
    s_headers = ["Table Name", "Column Name", "Data Type", "Constraints / Description"]
    s_widths = [Inches(1.3), Inches(1.5), Inches(1.2), Inches(2.7)]
    
    for c_idx, h_text in enumerate(s_headers):
        cell = schema_tbl.cell(0, c_idx)
        cell.width = s_widths[c_idx]
        set_cell_background(cell, "1E293B")
        set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.font.name = "Times New Roman"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    s_data = [
        ("transactions", "id", "INTEGER", "PRIMARY KEY AUTOINCREMENT"),
        ("transactions", "date", "TEXT", "NOT NULL (Format: YYYY-MM-DD)"),
        ("transactions", "type", "TEXT", "CHECK(type IN ('Income', 'Expense'))"),
        ("transactions", "category", "TEXT", "NOT NULL (e.g. Food, Rent, Travel)"),
        ("transactions", "amount", "REAL", "CHECK(amount > 0) Positive number"),
        ("transactions", "payment_mode", "TEXT", "DEFAULT 'UPI' (UPI, Cash, Card, Bank)"),
        ("budgets", "category", "TEXT", "PRIMARY KEY (Unique Category Name)"),
    ]
    for r_idx, row in enumerate(s_data, start=1):
        for c_idx, val in enumerate(row):
            cell = schema_tbl.cell(r_idx, c_idx)
            cell.width = s_widths[c_idx]
            set_cell_background(cell, "F8FAFC" if r_idx % 2 == 1 else "FFFFFF")
            set_cell_borders(cell, color="CBD5E1", sz="4", val="single")
            set_cell_margins(cell, top=40, bottom=40, left=60, right=60)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.name = "Times New Roman"
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_page_break()  # End Page 4

    # -------------------------------------------------------------
    # PAGE 5: METHODOLOGY, VISUALIZATIONS & CONCLUSION
    # -------------------------------------------------------------
    add_subheading(doc, "4. MATHEMATICAL METHODOLOGY & VISUAL OUTPUT", level=1)
    add_bullet_p(doc, "Mean = (1/N) * sum(x_i); Median = middle value of sorted expenses; Std Dev = sqrt((1/N)*sum((x_i - mean)^2)); 75th percentile (Q3) captures upper spend bounds.", "NumPy Descriptive Metrics: ")
    add_bullet_p(doc, "Variance = Monthly_Limit - Actual_Spent; Utilization % = (Spent / Limit) * 100; Status: Normal (<85%), Warning (85-100%), Over-Budget (>100%).", "Budget Variance Algorithm: ")

    img_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "reports_and_docs", "finance_dashboard_overview.png")
    if os.path.exists(img_path):
        try:
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(2)
            p_img.paragraph_format.space_after = Pt(2)
            p_img.add_run().add_picture(img_path, width=Inches(5.2))
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_after = Pt(4)
            r_cap = p_cap.add_run("Figure 4.1: Automated Matplotlib Visualizations (Category Donut & Monthly Bar Chart)")
            r_cap.font.name = "Times New Roman"
            r_cap.font.size = Pt(9.5)
            r_cap.font.italic = True
            r_cap.font.color.rgb = RGBColor(100, 116, 139)
        except Exception as e:
            add_body_p(doc, f"[Figure 4.1: Visualization Chart - {e}]")

    add_subheading(doc, "5. CONCLUSION & FUTURE SCOPE", level=1)
    add_body_p(doc, "The Personal Finance and Expense Analytics System delivers a complete, production-grade financial tracking platform in just 464 lines of modular Python code. Key competencies demonstrated include Python OOP, SQLite parameterized persistence, Pandas aggregations, NumPy statistics, Matplotlib embedded charts, and Tkinter GUI engineering. Future enhancements include OCR receipt scanning and predictive ML expenditure forecasting.")

    doc.add_page_break()  # End Page 5 -> Page 6 starts Source Code!

    # -------------------------------------------------------------
    # PAGES 6 TO 12: COMPLETE SOURCE CODE IMPLEMENTATION
    # -------------------------------------------------------------
    add_subheading(doc, "6. COMPLETE SOURCE CODE IMPLEMENTATION", level=1)
    add_body_p(doc, "This section presents the complete, exhaustive source code implementation of the Personal Finance and Expense Analytics System across all five modular project files (~464 lines total):")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 6.1 database.py
    with open(os.path.join(base_dir, "database.py"), "r", encoding="utf-8") as f:
        db_code = f.read()
    add_code_block(doc, "database.py (Database Manager & SQLite CRUD)", db_code)

    # 6.2 analytics.py
    with open(os.path.join(base_dir, "analytics.py"), "r", encoding="utf-8") as f:
        analytics_code = f.read()
    add_code_block(doc, "analytics.py (Pandas & NumPy Analytics Engine)", analytics_code)

    # 6.3 visualizer.py
    with open(os.path.join(base_dir, "visualizer.py"), "r", encoding="utf-8") as f:
        vis_code = f.read()
    add_code_block(doc, "visualizer.py (Matplotlib Chart Visualizer)", vis_code)

    # 6.4 gui.py
    with open(os.path.join(base_dir, "gui.py"), "r", encoding="utf-8") as f:
        gui_code = f.read()
    add_code_block(doc, "gui.py (Modern Tkinter Desktop Interface)", gui_code)

    # 6.5 main.py
    with open(os.path.join(base_dir, "main.py"), "r", encoding="utf-8") as f:
        main_code = f.read()
    add_code_block(doc, "main.py (Application Launcher & Seed Manager)", main_code)

    # Save documents
    out_path_1 = os.path.join(base_dir, "Personal_Finance_System_Project_Report.docx")
    out_path_2 = os.path.join(base_dir, "reports_and_docs", "Personal_Finance_System_Project_Report.docx")
    
    doc.save(out_path_1)
    doc.save(out_path_2)
    print(f"[+] Successfully generated project report at:\n  - {out_path_1}\n  - {out_path_2}")

if __name__ == "__main__":
    generate_report()
