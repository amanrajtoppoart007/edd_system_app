# tests/test_supplier.py
import unittest
from models.supplier import Supplier

class TestJob(unittest.TestCase):
    def test_supplier_creation(self):
        supplier = Supplier("Test Supplier","Test parts","Test Location")
        supplier.save()
        suppliers = Supplier.get_all()
        self.assertTrue(any(s[1] == "Test Supplier" for s in suppliers))

if __name__ == '__main__':
    unittest.main()