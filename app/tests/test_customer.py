# tests/test_customer.py
import unittest
from app.models.customer import Customer
from app.utils.utils import Utils

class TestJob(unittest.TestCase):
    def test_customer_creation(self):
        customer = Customer("Test Customer","Test parts","Test Location")
        customer.save()
        customers = Customer.get_all()
        self.assertTrue(any(c[1] == "Test Customer" for c in customers))

if __name__ == '__main__':
    unittest.main()