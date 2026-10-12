import tkinter as tk
from tkinter import ttk
from reports.tqm_report import dashboard_metrics, recent_audit

class DashboardFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=12)
        self.build()

    def build(self):
        ttk.Label(self, text='Quality Dashboard', font=('TkDefaultFont', 18, 'bold')).pack(anchor='w')
        ttk.Label(self, text='Q06 - Reduce Duplicate Entries | data-driven view of the process').pack(anchor='w', pady=(0, 12))
        self.cards = ttk.Frame(self)
        self.cards.pack(fill='x')
        self.labels = {}
        for key, title in [('books','Books'),('members','Members'),('active_issues','Active Issues'),('duplicate_defects','Duplicate Defects'),('validation_defects','Validation Defects')]:
            box = ttk.LabelFrame(self.cards, text=title, padding=10)
            box.pack(side='left', fill='x', expand=True, padx=4)
            label = ttk.Label(box, text='0', font=('TkDefaultFont', 20, 'bold'))
            label.pack()
            self.labels[key] = label
        audit_frame = ttk.LabelFrame(self, text='Recent Audit Activity', padding=8)
        audit_frame.pack(fill='both', expand=True, pady=12)
        self.tree = ttk.Treeview(audit_frame, columns=('Action','Entity','Details','Time'), show='headings')
        for c,w in [('Action',110),('Entity',100),('Details',430),('Time',160)]:
            self.tree.heading(c, text=c); self.tree.column(c, width=w)
        self.tree.pack(fill='both', expand=True)
        ttk.Button(self, text='Refresh Dashboard', command=self.refresh).pack(anchor='e')
        self.refresh()

    def refresh(self):
        metrics = dashboard_metrics()
        for key, label in self.labels.items():
            label.config(text=str(metrics[key]))
        for row in self.tree.get_children(): self.tree.delete(row)
        for row in recent_audit(): self.tree.insert('', 'end', values=row)
