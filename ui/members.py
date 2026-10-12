import tkinter as tk
from tkinter import ttk, messagebox
from services.member_service import add_member, delete_member, list_members
from utils.logger import log_error

class MembersFrame(ttk.Frame):
    def __init__(self,parent):
        super().__init__(parent,padding=10)
        self.vars={k:tk.StringVar() for k in ['Code','Name','Email','Phone']}
        self.build(); self.refresh()

    def build(self):
        form=ttk.LabelFrame(self,text='Members | Unique Identity + Confirmation',padding=10); form.pack(fill='x')
        for i,k in enumerate(self.vars):
            ttk.Label(form,text=k).grid(row=0,column=i,padx=5,sticky='w')
            ttk.Entry(form,textvariable=self.vars[k],width=24).grid(row=1,column=i,padx=5,pady=4)
        ttk.Button(form,text='Add Member',command=self.add_member).grid(row=2,column=1,pady=6)
        ttk.Button(form,text='Delete Selected Member',command=self.delete_selected).grid(row=2,column=2,pady=6)
        self.tree=ttk.Treeview(self,columns=('ID','Code','Name','Email','Phone'),show='headings')
        for c in self.tree['columns']:
            self.tree.heading(c,text=c); self.tree.column(c,width=155,anchor='center')
        self.tree.pack(fill='both',expand=True,pady=8)

    def refresh(self):
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in list_members(): self.tree.insert('', 'end', values=row)

    def add_member(self):
        if not messagebox.askyesno('Confirm Add','Add this member?'): return
        try:
            add_member(*(self.vars[k].get() for k in ['Code','Name','Email','Phone']))
            messagebox.showinfo('Success','Member added successfully.'); self.refresh()
        except Exception as exc:
            cat='Duplicate Prevention' if 'Duplicate' in str(exc) else 'Validation'
            log_error('MEM-ADD',cat,str(exc)); messagebox.showerror('Validation Error',str(exc))

    def delete_selected(self):
        sel=self.tree.selection()
        if not sel:
            log_error('DEL-MEMBER-NONE','UI Navigation','Delete member pressed without selection')
            messagebox.showwarning('Delete Member','Select a member first.'); return
        values=self.tree.item(sel[0])['values']
        member_id, code, name = values[0], values[1], values[2]
        if not messagebox.askyesno('Confirm Delete',f'Delete member {code} - {name}?'): return
        try:
            delete_member(member_id); messagebox.showinfo('Success','Member deleted successfully.'); self.refresh()
        except Exception as exc:
            log_error('DEL-MEMBER','Database',str(exc)); messagebox.showerror('Delete Error',str(exc))
