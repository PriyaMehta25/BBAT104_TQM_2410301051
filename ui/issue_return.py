import tkinter as tk
from tkinter import ttk, messagebox
from services.circulation_service import issue_book, return_book, list_issues
from utils.logger import log_error

class IssueReturnFrame(ttk.Frame):
    def __init__(self, parent, on_change=None):
        super().__init__(parent, padding=10)
        self.on_change = on_change
        self.vars = {k: tk.StringVar() for k in ['Book ID', 'Member ID', 'Issue ID']}
        self.build()
        self.refresh()

    def build(self):
        form=ttk.LabelFrame(self,text='Issue / Return | Process Control',padding=10); form.pack(fill='x')
        ttk.Label(form,text='Book ID').grid(row=0,column=0); ttk.Entry(form,textvariable=self.vars['Book ID'],width=16).grid(row=1,column=0,padx=8)
        ttk.Label(form,text='Member ID').grid(row=0,column=1); ttk.Entry(form,textvariable=self.vars['Member ID'],width=16).grid(row=1,column=1,padx=8)
        ttk.Button(form,text='Issue Book',command=self.issue).grid(row=1,column=2,padx=8)
        ttk.Label(form,text='Issue ID').grid(row=0,column=3); ttk.Entry(form,textvariable=self.vars['Issue ID'],width=16).grid(row=1,column=3,padx=8)
        ttk.Button(form,text='Return Book',command=self.return_).grid(row=1,column=4,padx=8)
        self.tree=ttk.Treeview(self,columns=('Issue ID','Book ID','Member ID','Issue Date','Return Date','Status'),show='headings')
        for c in self.tree['columns']:
            self.tree.heading(c,text=c); self.tree.column(c,width=130,anchor='center')
        self.tree.pack(fill='both',expand=True,pady=8)

    def refresh(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in list_issues(): self.tree.insert('', 'end', values=row)

    def issue(self):
        try:
            bid=int(self.vars['Book ID'].get()); mid=int(self.vars['Member ID'].get())
            if not messagebox.askyesno('Confirm Issue','Confirm issuing this book?'): return
            issue_book(bid,mid)
            self.refresh()
            if self.on_change:
                self.on_change()
            messagebox.showinfo('Success','Book issued successfully.')
        except Exception as exc:
            log_error('ISSUE','Issue/Return',str(exc)); messagebox.showerror('Issue Error',str(exc))

    def return_(self):
        try:
            iid=int(self.vars['Issue ID'].get())
            if not messagebox.askyesno('Confirm Return','Confirm returning this book?'): return
            return_book(iid)
            self.refresh()
            if self.on_change:
                self.on_change()
            messagebox.showinfo('Success','Book returned successfully.')
        except Exception as exc:
            log_error('RETURN','Issue/Return',str(exc)); messagebox.showerror('Return Error',str(exc))
