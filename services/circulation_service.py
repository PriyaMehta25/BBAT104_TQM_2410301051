from database.db import connect, fetchall, fetchone
from utils.logger import audit


def issue_book(book_id, member_id):
    con = connect()
    try:
        book = con.execute('SELECT copies FROM books WHERE book_id=?', (book_id,)).fetchone()
        if not book:
            raise ValueError('Book not found.')
        if book[0] <= 0:
            raise ValueError('No available copies.')
        if not con.execute('SELECT 1 FROM members WHERE member_id=?', (member_id,)).fetchone():
            raise ValueError('Member not found.')
        cur = con.execute("INSERT INTO issues(book_id,member_id,status) VALUES(?,?, 'Issued')", (book_id, member_id))
        issue_id = cur.lastrowid
        con.execute('UPDATE books SET copies=copies-1 WHERE book_id=?', (book_id,))
        con.commit()
    finally:
        con.close()
    audit('CREATE', 'ISSUE', issue_id, f'book_id={book_id}; member_id={member_id}')
    return issue_id


def return_book(issue_id):
    con = connect()
    try:
        row = con.execute('SELECT book_id,status FROM issues WHERE issue_id=?', (issue_id,)).fetchone()
        if not row:
            raise ValueError('Issue record not found.')
        if row[1] == 'Returned':
            raise ValueError('Book already returned.')
        con.execute("UPDATE issues SET return_date=date('now'), status='Returned' WHERE issue_id=?", (issue_id,))
        con.execute('UPDATE books SET copies=copies+1 WHERE book_id=?', (row[0],))
        con.commit()
    finally:
        con.close()
    audit('UPDATE', 'ISSUE', issue_id, 'Book returned')


def list_issues():
    return fetchall('SELECT issue_id,book_id,member_id,issue_date,return_date,status FROM issues ORDER BY issue_id DESC')
