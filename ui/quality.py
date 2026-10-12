"""TQM quality monitor for the Library Management System (Q06).

Shows live error-log counts separately from the project's analysis checksheet,
FMEA ratings, SIPOC map, CTQ requirements, SQC diagrams, and PDCA log.
"""

import math
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

from config.settings import ARTIFACTS_DIR
from database.db import fetchall
from reports.tqm_report import defect_summary


# Analysis dataset used in the project report. Update these counts with observed
# test results before final submission; they are separate from live error_logs.
CHECKSHEET_ROWS = [
    ("Duplicate book/member", 18, "High", "Controlled by Q06"),
    ("Invalid input", 14, "Medium", "Controlled by validation"),
    ("Issue/return error", 9, "High", "Controlled by checks"),
    ("Search mismatch", 6, "Medium", "Under monitoring"),
    ("UI navigation", 4, "Low", "Improvement item"),
    ("Database error", 3, "High", "Under monitoring"),
    ("Other", 2, "Low", "Monitoring"),
]

FMEA_ROWS = [
    ("Duplicate ISBN entered", "Duplicate book record", 9, 7, 3, 189,
     "UNIQUE ISBN + pre-add search", "High"),
    ("Duplicate member code", "Duplicate identity", 8, 6, 3, 144,
     "UNIQUE constraint + validation", "High"),
    ("Invalid email/phone", "Bad contact data", 6, 6, 4, 144,
     "Format validation", "High"),
    ("User confirms wrong delete", "Unintended data loss", 8, 3, 4, 96,
     "Confirmation dialog + audit log", "Medium"),
    ("No book copies available", "Invalid issue operation", 7, 4, 2, 56,
     "Availability check", "Medium"),
    ("Database file loss", "Service/data interruption", 9, 2, 6, 108,
     "Manual backup control", "Medium"),
]

SIPOC_ROWS = [
    ("Library staff / student", "Book/member details",
     "Enter → validate → search → confirm → save",
     "Accurate library records", "Students / librarian"),
    ("Librarian", "Issue/return request",
     "Check availability → confirm → update transaction",
     "Correct circulation status", "Member"),
    ("System admin / student", "Backup request",
     "Copy SQLite DB → verify file",
     "Recoverable database copy", "Project evaluator"),
]

PDCA_ROWS = [
    ("Plan", "Identify duplicate-entry defects; define CTQ as accurate, non-duplicated records.",
     "Defect log + CTQ tree"),
    ("Do", "Implement five Q06 controls in the application.",
     "Running Tkinter/SQLite application"),
    ("Check", "Review defect frequencies and Pareto priorities.",
     "Checksheet + Pareto chart"),
    ("Act", "Standardize validation/constraints and log the next improvement cycle.",
     "Updated code + PDCA log"),
]

DIAGRAMS = [
    ("System Architecture", "architecture.png"),
    ("DFD Level 0", "dfd_level0.png"),
    ("ER Diagram", "er_diagram.png"),
    ("SIPOC Map", "sipoc.png"),
    ("CTQ Tree", "ctq_tree.png"),
    ("Pareto Chart", "pareto_chart.png"),
    ("Fishbone Diagram", "fishbone.png"),
    ("PDCA Cycle", "pdca_cycle.png"),
]


class QualityFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        ttk.Label(
            self, text="TQM Quality Monitor", font=("TkDefaultFont", 18, "bold")
        ).pack(anchor="w")
        ttk.Label(
            self,
            text="Live logs, checksheet, FMEA risk ratings, process map and continuous-improvement evidence.",
            wraplength=1050,
        ).pack(anchor="w", pady=(0, 10))

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.summary_tab = ttk.Frame(self.notebook, padding=8)
        self.logs_tab = ttk.Frame(self.notebook, padding=8)
        self.checksheet_tab = ttk.Frame(self.notebook, padding=8)
        self.fmea_tab = ttk.Frame(self.notebook, padding=8)
        self.sipoc_tab = ttk.Frame(self.notebook, padding=8)
        self.ctq_tab = ttk.Frame(self.notebook, padding=8)
        self.diagrams_tab = ttk.Frame(self.notebook, padding=8)
        self.pdca_tab = ttk.Frame(self.notebook, padding=8)

        for frame, title in [
            (self.summary_tab, "Live Summary"),
            (self.logs_tab, "Live Error Log"),
            (self.checksheet_tab, "Checksheet"),
            (self.fmea_tab, "FMEA"),
            (self.sipoc_tab, "SIPOC"),
            (self.ctq_tab, "CTQ"),
            (self.diagrams_tab, "SQC Diagrams"),
            (self.pdca_tab, "PDCA"),
        ]:
            self.notebook.add(frame, text=title)

        self._build_summary()
        self._build_logs()
        self._build_checksheet()
        self._build_fmea()
        self._build_sipoc()
        self._build_ctq()
        self._build_diagrams()
        self._build_pdca()

        actions = ttk.Frame(self)
        actions.pack(fill="x", pady=(8, 0))
        ttk.Label(
            actions,
            text="Live log totals come from the current database. Checksheet values are the project analysis dataset.",
            wraplength=800,
        ).pack(side="left", anchor="w")
        ttk.Button(actions, text="Refresh Quality Data", command=self.refresh).pack(side="right")
        self.refresh()

    @staticmethod
    def _make_tree(parent, columns, widths, height=12):
        holder = ttk.Frame(parent)
        holder.pack(fill="both", expand=True)
        tree = ttk.Treeview(holder, columns=columns, show="headings", height=height)
        for col, width in zip(columns, widths):
            tree.heading(col, text=col)
            tree.column(col, width=width, minwidth=70, stretch=True)
        vertical = ttk.Scrollbar(holder, orient="vertical", command=tree.yview)
        horizontal = ttk.Scrollbar(holder, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        tree.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        holder.rowconfigure(0, weight=1)
        holder.columnconfigure(0, weight=1)
        return tree

    def _build_summary(self):
        ttk.Label(
            self.summary_tab,
            text="Counts calculated from the current database error_logs table.",
        ).pack(anchor="w", pady=(0, 8))
        self.summary_tree = self._make_tree(
            self.summary_tab, ("Category", "Frequency"), (450, 140), height=14
        )

    def _build_logs(self):
        ttk.Label(
            self.logs_tab,
            text="Individual logged events from error_logs. This is the live evidence trail.",
        ).pack(anchor="w", pady=(0, 8))
        self.logs_tree = self._make_tree(
            self.logs_tab,
            ("ID", "Code", "Category", "Message", "User", "Time"),
            (65, 110, 160, 440, 110, 175),
            height=14,
        )

    def _build_checksheet(self):
        ttk.Label(
            self.checksheet_tab,
            text=(
                "Project defect-analysis checksheet from the report. Confirm/update these frequencies "
                "against your observed testing results before final submission."
            ),
            wraplength=1000,
        ).pack(anchor="w", pady=(0, 8))
        self.checksheet_tree = self._make_tree(
            self.checksheet_tab,
            ("Defect Category", "Frequency", "Severity", "Status"),
            (270, 100, 110, 300),
            height=12,
        )
        for row in CHECKSHEET_ROWS:
            self.checksheet_tree.insert("", "end", values=row)

    def _build_fmea(self):
        ttk.Label(
            self.fmea_tab,
            text="RPN = Severity × Occurrence × Detection. Ratings are project risk-assessment values.",
        ).pack(anchor="w", pady=(0, 8))
        self.fmea_tree = self._make_tree(
            self.fmea_tab,
            ("Failure Mode", "Effect", "S", "O", "D", "RPN", "Mitigation", "Priority"),
            (200, 180, 45, 45, 45, 70, 260, 90),
            height=12,
        )
        for row in FMEA_ROWS:
            self.fmea_tree.insert("", "end", values=row)

    def _build_sipoc(self):
        ttk.Label(
            self.sipoc_tab,
            text="SIPOC = Suppliers, Inputs, Process, Outputs and Customers.",
        ).pack(anchor="w", pady=(0, 8))
        self.sipoc_tree = self._make_tree(
            self.sipoc_tab, ("Supplier", "Input", "Process", "Output", "Customer"),
            (190, 160, 300, 190, 180), height=10,
        )
        for row in SIPOC_ROWS:
            self.sipoc_tree.insert("", "end", values=row)
        ttk.Button(
            self.sipoc_tab, text="Open SIPOC Diagram", command=lambda: self.open_diagram("sipoc.png", "SIPOC Map")
        ).pack(anchor="e", pady=(8, 0))

    def _build_ctq(self):
        ttk.Label(self.ctq_tab, text="Critical to Quality (CTQ): accurate, non-duplicated library records.",
                  font=("TkDefaultFont", 12, "bold")).pack(anchor="w", pady=(0, 8))
        requirements = [
            ("Customer / librarian need", "Accurate and reliable library records"),
            ("Quality requirement", "Do not save duplicate book identifiers or member identifiers"),
            ("Technical control 1", "UNIQUE ISBN constraint at database level"),
            ("Technical control 2", "UNIQUE member code, email and phone constraints"),
            ("Technical control 3", "Pre-add validation and Search Before Add"),
            ("Technical control 4", "Confirmation dialogs for critical actions"),
            ("Evidence", "Duplicate attempt is blocked and logged; verify with live test screenshots"),
        ]
        tree = self._make_tree(self.ctq_tab, ("CTQ Level", "Requirement / Evidence"), (240, 780), height=10)
        for row in requirements:
            tree.insert("", "end", values=row)
        ttk.Button(
            self.ctq_tab, text="Open CTQ Tree Diagram", command=lambda: self.open_diagram("ctq_tree.png", "CTQ Tree")
        ).pack(anchor="e", pady=(8, 0))

    def _build_diagrams(self):
        ttk.Label(
            self.diagrams_tab,
            text="Open a prepared project diagram. Pareto/Fishbone visuals use the project's checksheet analysis dataset.",
            wraplength=1000,
        ).pack(anchor="w", pady=(0, 12))
        grid = ttk.Frame(self.diagrams_tab)
        grid.pack(anchor="nw", fill="x")
        for index, (label, filename) in enumerate(DIAGRAMS):
            button = ttk.Button(
                grid, text=f"Open {label}", width=25,
                command=lambda f=filename, t=label: self.open_diagram(f, t),
            )
            button.grid(row=index // 2, column=index % 2, sticky="ew", padx=6, pady=6)
        grid.columnconfigure(0, weight=1)
        grid.columnconfigure(1, weight=1)

    def _build_pdca(self):
        ttk.Label(
            self.pdca_tab,
            text="PDCA = Plan, Do, Check, Act. Use this cycle to document iterative quality improvements.",
        ).pack(anchor="w", pady=(0, 8))
        self.pdca_tree = self._make_tree(
            self.pdca_tab, ("Phase", "Action", "Evidence"), (100, 600, 300), height=10
        )
        for row in PDCA_ROWS:
            self.pdca_tree.insert("", "end", values=row)
        ttk.Button(
            self.pdca_tab, text="Open PDCA Diagram", command=lambda: self.open_diagram("pdca_cycle.png", "PDCA Cycle")
        ).pack(anchor="e", pady=(8, 0))

    def _refresh_tree(self, tree, rows):
        for item in tree.get_children():
            tree.delete(item)
        for row in rows:
            tree.insert("", "end", values=row)

    def refresh(self):
        """Reload live database-backed quality evidence without changing report baselines."""
        try:
            self._refresh_tree(self.summary_tree, defect_summary())
            log_rows = fetchall(
                "SELECT error_id, error_code, category, message, user_name, log_time "
                "FROM error_logs ORDER BY error_id DESC LIMIT 500"
            )
            self._refresh_tree(self.logs_tree, log_rows)
        except Exception as exc:
            messagebox.showerror("Quality Data Error", str(exc), parent=self)

    def open_diagram(self, filename, title):
        path = Path(ARTIFACTS_DIR) / filename
        if not path.exists():
            messagebox.showerror("Diagram Not Found", f"Could not find the diagram file:\n{path}", parent=self)
            return
        try:
            viewer = tk.Toplevel(self)
            viewer.title(title)
            viewer.geometry("1050x720")
            viewer.minsize(600, 400)
            photo = tk.PhotoImage(master=viewer, file=str(path))
            factor = max(1, math.ceil(photo.width() / 1100), math.ceil(photo.height() / 650))
            if factor > 1:
                photo = photo.subsample(factor, factor)
            canvas = tk.Canvas(viewer, highlightthickness=0)
            xbar = ttk.Scrollbar(viewer, orient="horizontal", command=canvas.xview)
            ybar = ttk.Scrollbar(viewer, orient="vertical", command=canvas.yview)
            canvas.configure(xscrollcommand=xbar.set, yscrollcommand=ybar.set)
            canvas.grid(row=0, column=0, sticky="nsew")
            ybar.grid(row=0, column=1, sticky="ns")
            xbar.grid(row=1, column=0, sticky="ew")
            viewer.rowconfigure(0, weight=1)
            viewer.columnconfigure(0, weight=1)
            canvas.create_image(0, 0, anchor="nw", image=photo)
            canvas.configure(scrollregion=(0, 0, photo.width(), photo.height()))
            viewer._diagram_image = photo
        except tk.TclError as exc:
            messagebox.showerror("Diagram Error", f"Could not display {filename}:\n{exc}", parent=self)
