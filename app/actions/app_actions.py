import sys
import unittest
import os # Import the os module
from models.customer import Customer
from models.equipment import Equipment
from models.job import Job
from models.administrator import Administrator
from models.technician import Technician
from app.database.db import Database
from models.supplier import Supplier

class AppAction:
    def __init__(self):
        self.current_user = None
        self.db = Database()

    def start(self):
        while True:
            try:
                print("\n--- EDD Technologies ---")
                print("1. Login as Administrator")
                print("2. Login as Technician")
                print("3. Login as Customer")
                print("4. Test Modules")
                print("5. Exit")
                choice = input("Choose an option: ")
                if choice == '1':
                    name = input("Enter admin name: ")
                    self.current_user = Administrator(name)
                    self.admin_menu()
                elif choice == '2':
                    email = input("Enter technician email: ")
                    technician = Technician.find_by_email(email)
                    if technician:
                        self.current_user = technician
                        self.technician_menu()
                    else:
                        print("Technician not found.")
                elif choice == '3':
                    email = input("Enter your email: ")
                    customer = Customer.find_by_email(email)
                    if customer:
                        self.current_user = customer
                        self.customer_menu()
                    else:
                        print("Customer not found. Please register as walk-in.")
                elif choice == '4':
                    self.run_tests()
                elif choice == '5':
                    print("Goodbye!")
                    sys.exit()
                else:
                    print("Invalid option.")
            except KeyboardInterrupt:
                print("\n[!] Returning to main menu.")

    def admin_menu(self):
        while True:
            try:
                print("\n--- Admin Menu ---")
                print("1. Register Walk-in Customer")
                print("2. List All Jobs")
                print("3. Allocate Job to Technician")
                print("4. Add New Technician")
                print("5. View Assessed Jobs and Add Cost")
                print("6. Manage Suppliers")
                print("7. Logout")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.register_walkin_customer()
                elif choice == '2':
                    self.list_jobs()
                elif choice == '3':
                    self.allocate_job()
                elif choice == '4':
                    self.add_technician()
                elif choice == '5':
                    self.view_assessed_jobs_and_add_cost()
                elif choice == '6':
                    self.manage_suppliers()
                elif choice == '7':
                    break
                else:
                    print("Invalid choice")
            except KeyboardInterrupt:
                print("\n[!] Returning to admin menu.")
                break



    def remove_suppliers(self):
        ids_input = input("Enter supplier IDs to remove (comma separated): ")
        try:
            ids = [int(i.strip()) for i in ids_input.split(",") if i.strip().isdigit()]
            Supplier.remove_suppliers_by_ids(ids)
            print("Suppliers removed successfully.")
        except Exception as e:
            print(f"Error removing suppliers: {e}")

    def manage_suppliers(self):
        try:
            print("\n--- Manage Suppliers ---")
            print("1. Add Supplier")
            print("2. View All Suppliers")
            print("3. Remove Suppliers")
            sub_choice = input("Choose an option: ")

            if sub_choice == '1':
                name = input("Enter supplier name: ")
                part_type = input("Enter part type: ")
                location = input("Enter supplier location: ")
                supplier = Supplier(name, part_type, location)
                supplier.save()
                print("Supplier added successfully.")
            elif sub_choice == '2':
                suppliers = Supplier.get_all()
                if suppliers:
                    for s in suppliers:
                        print(f"ID: {s[0]}, Name: {s[1]}, Part Type: {s[2]}, Location: {s[3]}")
                else:
                    print("No suppliers found.")
            elif sub_choice == '3': 
                self.remove_suppliers()       
            else:
                print("Invalid option.")
        except Exception as e:
            print(f"[!] Error: {e}")



    def add_technician(self):
        try:
            name = input("Enter technician name: ")
            email = input("Enter technician email: ")
            expertise = input("Enter technician expertise: ")
            technician = Technician(name,email, expertise)
            technician.save()
            print(f"Technician '{name}' with '{email}' added successfully.")
        except Exception as e:
            print(f"[!] Error adding technician: {e}")

    def register_walkin_customer(self):
        try:
            name = input("Enter customer name: ")
            email = input("Enter email: ")
            equipment_type = input("Enter equipment type: ")
            serial = input("Enter serial number: ")

            customer = Customer(name, email)
            customer_id = customer.save()
            equipment = Equipment(customer_id, equipment_type, serial)
            equipment.save()
            print(f"Customer {name} and equipment details saved.")
        except Exception as e:
            print(f"Error while registering customer: {e}")

    def list_jobs(self):
        jobs = Job.get_all()
        for job in jobs:
            print(f"Job ID: {job[0]}, Customer: {job[6]} , Description: {job[3]}, Status: {job[4]} , Cost: {job[5]}")


    def allocate_job(self):
        try:
            equipment_id = input("Enter equipment ID to allocate job: ")
            technician_id = input("Enter technician ID to allocate job: ")
            description = input("Enter job description: ")
            job = Job(description, technician_id=technician_id,equipment_id=equipment_id)
            job.save()
            print(f"Job created with ID: {job.id}")
        except Exception as e:
            print(f"Error while allocating job: {e}")

    def technician_menu(self):
        while True:
            try:
                print("\n--- Technician Menu ---")
                print("1. View My Assigned Jobs")
                print("2. Mark Jobs as Assessed")
                print("3. Manage Suppliers")
                print("4. Logout")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.list_jobs_for_technician()
                elif choice == '2':
                    self.change_job_status()
                elif choice == '3':
                    self.manage_suppliers()
                elif choice == '4':
                    break  
                else:
                    print("Invalid choice")
            except KeyboardInterrupt:
                print("\n[!] Returning to technician menu.")
                break

    def list_jobs_for_technician(self):
        try:
            technician_id = self.current_user.get_id()
            jobs = Job.get_by_technician(technician_id)
            if jobs:
                for job in jobs:
                    print(f"\nJob ID: {job[0]}, Description: {job[1]}, Status: {job[2]}")
                    print(f"  Equipment: {job[3]}, Serial: {job[4]}")
            else:
                print("No jobs assigned to you.")
        except Exception as e:
            print(f"Error while listing jobs: {e}")

    def change_job_status(self):
        ids = input("Enter Job IDs to mark as 'Job Assessed' (comma-separated): ")
        try:
            job_ids = [int(x.strip()) for x in ids.split(",") if x.strip().isdigit()]
            if Job.update_status_for_technician(job_ids, self.current_user.id):
                print("Selected jobs updated to 'Job Assessed'.")
        except ValueError:
            print("Invalid input. Enter numeric Job IDs separated by commas.")

    def customer_menu(self):
        while True:
            try:
                print("\n--- Customer Menu ---")
                print("1. Book Equipment Repair")
                print("2. Logout")
                choice = input("Choose an option: ")
                if choice == '1':
                    self.book_equipment_repair()
                elif choice == '2':
                    break
                else:
                    print("Invalid choice")
            except KeyboardInterrupt:
                print("\n[!] Returning to customer menu.")
                break

    def book_equipment_repair(self):
        try:
            equipment_type = input("Enter equipment type: ")
            serial = input("Enter serial number: ")
            customer_id = self.current_user.get_id()
            equipment = Equipment(customer_id, equipment_type, serial)
            equipment.save(customer_id, equipment_type, serial)
            print("Equipment registered for repair.")
        except Exception as e:
            print(f"Error while booking equipment: {e}")


    def view_assessed_jobs_and_add_cost(self):
        try:
            assessed_jobs = Job.get_assessed_jobs()
            if not assessed_jobs:
                print("No assessed jobs found.")
                return

            print("\n--- Assessed Jobs ---")
            for job in assessed_jobs:
                print(f"Job ID: {job[0]}, Equipment ID: {job[1]}, Technician ID: {job[2]}, Description: {job[3]}, Status: {job[4]}, Cost: {job[5] if len(job) > 5 else 'N/A'}")

            job_id = input("Enter Job ID to add cost (or press Enter to skip): ").strip()
            if job_id:
                cost = input("Enter cost amount: ").strip()
                Job.update_cost(int(job_id), float(cost))
                print("Cost updated.")
        except Exception as e:
            print(f"[!] Error: {e}")

    def run_tests(self):
            """Discovers and runs tests in the 'tests' directory."""
            print("\n--- Running Unit Tests ---")
            # Define the directory where tests are located
            # Assumes 'tests' directory is in the same parent directory as this script
            # Adjust the path if your structure is different
            test_dir = os.path.join(os.path.dirname(__file__), '..', 'tests')
            if not os.path.isdir(test_dir):
                # Fallback: Assume 'tests' is a direct subdirectory
                test_dir = os.path.join(os.path.dirname(__file__), 'tests')

            if not os.path.isdir(test_dir):
                print(f"Error: Test directory not found at expected locations.")
                print(f"Looked in: {os.path.join(os.path.dirname(__file__), '..', 'tests')} and {os.path.join(os.path.dirname(__file__), 'tests')}")
                return

            print(f"Discovering tests in: {test_dir}")
            # Discover tests
            loader = unittest.TestLoader()
            suite = loader.discover(test_dir, pattern='test_*.py') # Standard pattern for test files

            if suite.countTestCases() == 0:
                print("No tests found.")
                return

            # Run the tests
            runner = unittest.TextTestRunner(verbosity=2) # verbosity=2 provides more detailed output
            result = runner.run(suite)

            print("--- Test Run Complete ---")
            # Optional: Print summary or handle results further
            if result.wasSuccessful():
                print("All tests passed successfully!")
            else:
                print("Some tests failed.")
            input("Press Enter to return to the main menu...") # Pause to see results

