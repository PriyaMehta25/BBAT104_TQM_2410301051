from database.db import connect, fetchall, fetchone
from utils.logger import audit
from utils.validators import required, year, copies


def add_book(isbn, title, author, category, publication_year, copy_count):
    isbn = required(isbn, 'ISBN')
    if not isbn.replace('-', '').isalnum():
        raise ValueError('ISBN may contain letters, digits and hyphens only.')
    title = required(title, 'Title')
    author = required(author, 'Author')
    category = required(category, 'Category')
    publication_year = year(publication_year)
    copy_count = copies(copy_count)
    con = connect()
    try:
        if con.execute('SELECT 1 FROM books WHERE isbn=?', (isbn,)).fetchone():
            raise ValueError('A matching ISBN already exists. Add operation stopped.')
        cur = con.execute('INSERT INTO books(isbn,title,author,category,year,copies) VALUES(?,?,?,?,?,?)',
                          (isbn, title, author, category, publication_year, copy_count))
        con.commit()
        book_id = cur.lastrowid
    finally:
        con.close()
    audit('CREATE', 'BOOK', book_id, f'ISBN={isbn}; title={title}')
    return book_id


def delete_book(book_id):
    con = connect()
    try:
        if con.execute('SELECT 1 FROM issues WHERE book_id=?', (book_id,)).fetchone():
            raise ValueError('Cannot delete a book referenced by an issue record.')
        con.execute('DELETE FROM books WHERE book_id=?', (book_id,))
        con.commit()
    finally:
        con.close()
    audit('DELETE', 'BOOK', book_id, 'Book deleted')


def list_books():
    return fetchall('SELECT book_id,isbn,title,author,category,year,copies FROM books ORDER BY book_id')


def search_books(term):
    term = str(term).strip()
    like = f'%{term}%'
    return fetchall(
        'SELECT book_id,isbn,title,author,category,year,copies FROM books '
        'WHERE isbn LIKE ? OR title LIKE ? OR author LIKE ? ORDER BY title',
        (like, like, like),
    )


def get_book(book_id):
    return fetchone('SELECT book_id,isbn,title,author,category,year,copies FROM books WHERE book_id=?', (book_id,))
