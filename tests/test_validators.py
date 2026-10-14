import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from database.schema import init_db
from services.book_service import add_book, list_books
from services.member_service import add_member, list_members
from utils.validators import required, year, copies, email, phone


class ValidatorTests(unittest.TestCase):

    def test_required(self):
        self.assertEqual(required("Book", "Title"), "Book")

        with self.assertRaises(ValueError):
            required("", "Title")

    def test_year(self):
        self.assertEqual(year("2022"), 2022)

        with self.assertRaises(ValueError):
            year("999")

    def test_copies(self):
        self.assertEqual(copies("2"), 2)

        with self.assertRaises(ValueError):
            copies("-1")

    def test_email_phone(self):
        self.assertEqual(email("a@example.com"), "a@example.com")
        self.assertEqual(phone("9876500001"), "9876500001")

        with self.assertRaises(ValueError):
            email("bad")

        with self.assertRaises(ValueError):
            phone("123")


class Q06DuplicatePreventionTests(unittest.TestCase):

    def setUp(self):
        # Create a temporary test database.
        self.temp_dir = tempfile.TemporaryDirectory()
        test_db = Path(self.temp_dir.name) / "test_library.db"

        # Keep tests separate from your actual library database.
        self.db_patcher = patch("database.db.DB_PATH", test_db)
        self.db_patcher.start()

        init_db()

    def tearDown(self):
        self.db_patcher.stop()
        self.temp_dir.cleanup()

    def test_valid_book_is_added(self):
        book_id = add_book(
            "978-000000099",
            "Test Book",
            "Test Author",
            "Testing",
            "2022",
            "1"
        )

        self.assertGreater(book_id, 0)
        self.assertEqual(len(list_books()), 1)

    def test_duplicate_isbn_is_rejected(self):
        add_book(
            "978-000000099",
            "First Book",
            "Author One",
            "Testing",
            "2022",
            "1"
        )

        with self.assertRaisesRegex(ValueError, "matching ISBN"):
            add_book(
                "978-000000099",
                "Second Book",
                "Author Two",
                "Testing",
                "2023",
                "1"
            )

        self.assertEqual(len(list_books()), 1)

    def test_invalid_book_year_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "publication year"):
            add_book(
                "978-000000098",
                "Test Book",
                "Test Author",
                "Testing",
                "999",
                "1"
            )

        self.assertEqual(len(list_books()), 0)

    def test_valid_member_is_added(self):
        member_id = add_member(
            "MTEST01",
            "Test Member",
            "test1@example.com",
            "9000000001"
        )

        self.assertGreater(member_id, 0)
        self.assertEqual(len(list_members()), 1)

    def test_duplicate_member_code_is_rejected(self):
        add_member(
            "MTEST01", "Member One",
            "one@example.com", "9000000001"
        )

        with self.assertRaisesRegex(ValueError, "Duplicate member details"):
            add_member(
                "MTEST01", "Member Two",
                "two@example.com", "9000000002"
            )

        self.assertEqual(len(list_members()), 1)

    def test_duplicate_member_email_is_rejected(self):
        add_member(
            "MTEST01", "Member One",
            "one@example.com", "9000000001"
        )

        with self.assertRaisesRegex(ValueError, "Duplicate member details"):
            add_member(
                "MTEST02", "Member Two",
                "one@example.com", "9000000002"
            )

        self.assertEqual(len(list_members()), 1)

    def test_duplicate_member_phone_is_rejected(self):
        add_member(
            "MTEST01", "Member One",
            "one@example.com", "9000000001"
        )

        with self.assertRaisesRegex(ValueError, "Duplicate member details"):
            add_member(
                "MTEST02", "Member Two",
                "two@example.com", "9000000001"
            )

        self.assertEqual(len(list_members()), 1)

    def test_invalid_member_email_is_rejected(self):
        with self.assertRaisesRegex(ValueError, "valid email"):
            add_member(
                "MTEST01", "Test Member",
                "not-an-email", "9000000001"
            )

        self.assertEqual(len(list_members()), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)