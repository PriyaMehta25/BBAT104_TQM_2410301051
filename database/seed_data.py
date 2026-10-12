from database.schema import init_db
from services.book_service import add_book
from services.member_service import add_member


def seed():
    init_db()
    books = [
        ('978-000000001','Introduction to Algorithms','Cormen','Computer Science',2022,3),
        ('978-000000002','Database System Concepts','Korth','Database',2021,2),
        ('978-000000003','Software Engineering','Pressman','Software Engineering',2020,4),
        ('978-000000004','Total Quality Management','Besterfield','Management',2019,2),
        ('978-000000005','Computer Networks','Tanenbaum','Networking',2021,3),
    ]
    members = [
        ('M001','Aarav Sharma','aarav@example.com','9876500001'),
        ('M002','Ananya Singh','ananya@example.com','9876500002'),
        ('M003','Rahul Verma','rahul@example.com','9876500003'),
        ('M004','Sneha Gupta','sneha@example.com','9876500004'),
        ('M005','Vikram Joshi','vikram@example.com','9876500005'),
    ]
    for row in books:
        try: add_book(*row)
        except ValueError: pass
    for row in members:
        try: add_member(*row)
        except ValueError: pass
    print('Seed data loaded.')


if __name__ == '__main__':
    seed()
