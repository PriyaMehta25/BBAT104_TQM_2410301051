from database.db import connect, fetchall
from utils.logger import audit
from utils.validators import required, email, phone


def add_member(code, name, member_email, member_phone):
    code = required(code, 'Member code')
    name = required(name, 'Name')
    member_email = email(member_email)
    member_phone = phone(member_phone)
    con = connect()
    try:
        if con.execute('SELECT 1 FROM members WHERE member_code=? OR email=? OR phone=?',
                       (code, member_email, member_phone)).fetchone():
            raise ValueError('Duplicate member details detected.')
        cur = con.execute('INSERT INTO members(member_code,name,email,phone) VALUES(?,?,?,?)',
                          (code, name, member_email, member_phone))
        con.commit()
        member_id = cur.lastrowid
    finally:
        con.close()
    audit('CREATE', 'MEMBER', member_id, f'Code={code}; name={name}')
    return member_id


def delete_member(member_id):
    con = connect()
    try:
        if con.execute('SELECT 1 FROM issues WHERE member_id=?', (member_id,)).fetchone():
            raise ValueError('Cannot delete a member referenced by an issue record.')
        con.execute('DELETE FROM members WHERE member_id=?', (member_id,))
        con.commit()
    finally:
        con.close()
    audit('DELETE', 'MEMBER', member_id, 'Member deleted')


def list_members():
    return fetchall('SELECT member_id,member_code,name,email,phone FROM members ORDER BY member_id')
