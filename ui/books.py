import tkinter as tk
from tkinter import ttk, messagebox
from services.book_service import add_book, delete_book, list_books
from services.search_service import search_before_add
from utils.logger import log_error

class BooksFrame(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padding=10)
        self.vars = {k: tk.StringVar() for k in ['ISBN','Title','Author','Category','Year','Copies','Search']}
        self.build()
        self.refresh()

    def build(self):
        form = ttk.LabelFrame(self, text='Books | Q06 Duplicate Prevention', padding=10)
        form.pack(fill='x')
        labels = ['ISBN','Title','Author','Category','Year','Copies']
        for i,k in enumerate(labels):
            ttk.Label(form, text=k).grid(row=0,column=i,padx=4,sticky='w')
            ttk.Entry(form, textvariable=self.vars[k], width=17).grid(row=1,column=i,padx=4,pady=4)
        ttk.Button(form, text='Search Before Add', command=self.search_before_add).grid(row=2,column=0,columnspan=2,pady=6)
        ttk.Button(form, text='Add Book', command=self.add_book).grid(row=2,column=2,columnspan=2,pady=6)
        ttk.Button(form, text='Delete Selected', command=self.delete_selected).grid(row=2,column=4,columnspan=2,pady=6)
        search = ttk.Frame(self, padding=(0,8,0,0)); search.pack(fill='x')
        ttk.Label(search, text='Quick Search').pack(side='left')
        ttk.Entry(search, textvariable=self.vars['Search'], width=35).pack(side='left', padx=6)
        ttk.Button(search, text='Find', command=self.quick_search).pack(side='left')
        self.tree = ttk.Treeview(self, columns=('ID','ISBN','Title','Author','Category','Year','Copies'), show='headings')
        for c in self.tree['columns']:
            self.tree.heading(c,text=c); self.tree.column(c,width=130,anchor='center')
        self.tree.pack(fill='both', expand=True, pady=8)

    def refresh(self, rows=None):
        if rows is None: rows = list_books()
        for item in self.tree.get_children(): self.tree.delete(item)
        for row in rows: self.tree.insert('', 'end', values=row)

    def search_before_add(self):
        term = self.vars['ISBN'].get().strip() or self.vars['Title'].get().strip()
        if not term:
            messagebox.showwarning('Search', 'Enter ISBN or Title first.')
            return
        rows = search_before_add(term)
        if rows:
            messagebox.showinfo('Potential Existing Record', f'Potential existing record(s) found: {len(rows)}\nReview the table before adding.')
        else:
            messagebox.showinfo('Search', 'No matching record found. Continue with validation and confirmation.')

    def add_book(self):
        isbn = self.vars['ISBN'].get().strip()
        if search_before_add(isbn):
            log_error('DUP-ISBN','Duplicate Prevention',f'Duplicate ISBN attempt: {isbn}')
            messagebox.showwarning('Duplicate Prevention', 'A matching ISBN already exists. Add operation stopped.')
            return
        if not messagebox.askyesno('Confirm Add', 'Add this book to the library?'):
            return
        try:
            add_book(*(self.vars[k].get() for k in ['ISBN','Title','Author','Category','Year','Copies']))
            messagebox.showinfo('Success','Book added successfully.')
            self.refresh()
        except Exception as exc:
            category = 'Duplicate Prevention' if 'Duplicate' in str(exc) else 'Validation'
            log_error('BOOK-ADD', category, str(exc))
            messagebox.showerror('Validation Error', str(exc))

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            log_error('DEL-NONE','UI Navigation','Delete book pressed without selecting a row')
            messagebox.showwarning('Delete','Select a book first.'); return
        book_id = self.tree.item(sel[0])['values'][0]
        if not messagebox.askyesno('Confirm Delete','Delete selected book?'): return
        try:
            delete_book(book_id); messagebox.showinfo('Success','Book deleted successfully.'); self.refresh()
        except Exception as exc:
            log_error('DEL-BOOK','Database',str(exc)); messagebox.showerror('Delete Error',str(exc))

    def quick_search(self):
        self.refresh(search_before_add(self.vars['Search'].get()))
