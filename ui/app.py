import tkinter as tk
from tkinter import ttk, messagebox
from config.settings import APP_NAME, QUALITY_GOAL, VERSION
from ui.dashboard import DashboardFrame
from ui.books import BooksFrame
from ui.members import MembersFrame
from ui.issue_return import IssueReturnFrame
from ui.quality import QualityFrame
from utils.backup import create_backup

class LibraryApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title(f'{APP_NAME} - {QUALITY_GOAL}')
        self.geometry('1180x760')
        self.minsize(1000,650)
        self.protocol('WM_DELETE_WINDOW', self.on_close)
        self.style=ttk.Style(self)
        self.style.configure('TButton',padding=6)
        self.style.configure('Treeview',rowheight=28)
        self.build_ui()

    def build_ui(self):
        header=ttk.Frame(self,padding=10); header.pack(fill='x')
        ttk.Label(header,text=APP_NAME,font=('TkDefaultFont',19,'bold')).pack(side='left')
        ttk.Label(header,text=f'  |  {QUALITY_GOAL}  |  v{VERSION}').pack(side='left')
        ttk.Button(header,text='Backup Database',command=self.backup).pack(side='right')

        tabs=ttk.Notebook(self); tabs.pack(fill='both',expand=True,padx=10,pady=(0,10))
        self.dashboard = DashboardFrame(tabs)
        self.books = BooksFrame(tabs)
        self.members = MembersFrame(tabs)
        self.issue_return = IssueReturnFrame(tabs, on_change=self.refresh_after_circulation)
        self.quality = QualityFrame(tabs)
        tabs.add(self.dashboard,text='Dashboard')
        tabs.add(self.books,text='Books')
        tabs.add(self.members,text='Members')
        tabs.add(self.issue_return,text='Issue / Return')
        tabs.add(self.quality,text='Quality')
        self.tabs=tabs

    def backup(self):
        try:
            target=create_backup(); messagebox.showinfo('Backup',f'Backup created:\n{target.name}')
            self.dashboard.refresh()
        except Exception as exc:
            messagebox.showerror('Backup Error',str(exc))

    def refresh_after_circulation(self):
        """Refresh screens affected when a book is issued or returned."""
        self.books.refresh()
        self.dashboard.refresh()
        self.quality.refresh()

    def refresh_everything(self):
        self.dashboard.refresh()
        self.books.refresh()
        self.members.refresh()
        self.issue_return.refresh()
        self.quality.refresh()

    def on_close(self):
        try:
            create_backup()
        except Exception:
            pass
        self.destroy()
