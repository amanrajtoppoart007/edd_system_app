# tests/test_customer.py
import unittest
from app.models.technician import Technician
from app.utils.utils import Utils

class TestJob(unittest.TestCase):
    def test_technician_creation(self):
        utils = Utils
        technician = Technician("Test Technician",utils.generate_random_email(),"Test")
        technician.save()
        technicians = Technician.get_all()
        self.assertTrue(any(t[1] == "Test Technician" for t in technicians))

if __name__ == '__main__':
    unittest.main()