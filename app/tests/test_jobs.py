# tests/test_jobs.py
import unittest
from app.models.job import Job
from app.models.customer import Customer
from app.models.technician import Technician
from app.models.equipment import Equipment
from app.utils.utils import Utils

class TestJob(unittest.TestCase):
    def test_job_creation(self):
        utils = Utils
        customer = Customer('Guest Customer',utils.generate_random_email())
        customer_id = customer.save()
        technician = Technician('Guest Technician',utils.generate_random_email(),'tech')
        technician_id = technician.save()
        equipment = Equipment(customer_id=customer_id,type="laptop",serial_number=12345) 
        equipment_id = equipment.save()
        job = Job("Replace battery","Job Created",technician_id,equipment_id)
        job.save()
        jobs = Job.get_all()
        self.assertTrue(any(j[3] == "Replace battery" for j in jobs))

if __name__ == '__main__':
    unittest.main()