from database.schema import init_db
from database.migrations import run_migrations
from ui.app import LibraryApp

if __name__ == '__main__':
    init_db()
    run_migrations()
    app = LibraryApp()
    app.mainloop()
