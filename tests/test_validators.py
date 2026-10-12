import unittest
from utils.validators import required, year, copies, email, phone

class ValidatorTests(unittest.TestCase):
    def test_required(self):
        self.assertEqual(required('Book','Title'),'Book')
        with self.assertRaises(ValueError): required('','Title')
    def test_year(self):
        self.assertEqual(year('2022'),2022)
        with self.assertRaises(ValueError): year('999')
    def test_copies(self):
        self.assertEqual(copies('2'),2)
        with self.assertRaises(ValueError): copies('-1')
    def test_email_phone(self):
        self.assertEqual(email('a@example.com'),'a@example.com')
        with self.assertRaises(ValueError): email('bad')
        self.assertEqual(phone('9876500001'),'9876500001')
        with self.assertRaises(ValueError): phone('123')

if __name__ == '__main__': unittest.main()
