from database.db import connect


def init_db():
    con = connect()
    con.executescript('''
    CREATE TABLE IF NOT EXISTS schema_version(
        version INTEGER PRIMARY KEY
    );

    CREATE TABLE IF NOT EXISTS books(
        book_id INTEGER PRIMARY KEY AUTOINCREMENT,
        isbn TEXT NOT NULL UNIQUE,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        category TEXT NOT NULL,
        year INTEGER NOT NULL CHECK(year BETWEEN 1000 AND 2100),
        copies INTEGER NOT NULL DEFAULT 1 CHECK(copies >= 0)
    );

    CREATE TABLE IF NOT EXISTS members(
        member_id INTEGER PRIMARY KEY AUTOINCREMENT,
        member_code TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        phone TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS issues(
        issue_id INTEGER PRIMARY KEY AUTOINCREMENT,
        book_id INTEGER NOT NULL,
        member_id INTEGER NOT NULL,
        issue_date TEXT NOT NULL DEFAULT (date('now')),
        return_date TEXT,
        status TEXT NOT NULL CHECK(status IN ('Issued','Returned')),
        FOREIGN KEY(book_id) REFERENCES books(book_id),
        FOREIGN KEY(member_id) REFERENCES members(member_id)
    );

    CREATE TABLE IF NOT EXISTS audit_logs(
        log_id INTEGER PRIMARY KEY AUTOINCREMENT,
        action TEXT NOT NULL,
        entity TEXT NOT NULL,
        entity_id INTEGER,
        details TEXT,
        user_name TEXT DEFAULT 'student',
        log_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE TABLE IF NOT EXISTS error_logs(
        error_id INTEGER PRIMARY KEY AUTOINCREMENT,
        error_code TEXT NOT NULL,
        category TEXT NOT NULL,
        message TEXT NOT NULL,
        user_name TEXT DEFAULT 'student',
        log_time TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
    );

    CREATE INDEX IF NOT EXISTS idx_books_title ON books(title);
    CREATE INDEX IF NOT EXISTS idx_books_isbn ON books(isbn);
    CREATE INDEX IF NOT EXISTS idx_members_code ON members(member_code);
    CREATE INDEX IF NOT EXISTS idx_issues_status ON issues(status);
    ''' )
    con.execute('INSERT OR IGNORE INTO schema_version(version) VALUES (1)')
    con.commit()
    con.close()
