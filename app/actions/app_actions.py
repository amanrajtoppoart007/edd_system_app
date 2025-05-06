import sys
import unittest
import os
from app.models.customer import Customer
from app.models.equipment import Equipment
from app.models.job import Job
from app.models.administrator import Administrator
from app.models.technician import Technician
from app.db.db import DB
from app.models.supplier import Supplier

class AppAction:
    def __init__(self):
        self.active_user = None
        self.data_store = DB()

    def start(self):
        while True:
            try:
                print("\n--- Tech Solutions Portal ---")
                options = {
                    "1": "Admin Login",
                    "2": "Technician Access",
                    "3": "Customer Portal",
                    "4": "Execute Module Tests",
                    "5": "Exit Application"
                }
                for key, value in options.items():
                    print(f"{key}. {value}")

                selection = input("Select an action: ")
                if selection == '1':
                    admin_name = input("Enter administrator username: ")
                    self.active_user = Administrator(admin_name)
                    self._admin_operations()
                elif selection == '2':
                    tech_email = input("Enter technician email address: ")
                    technician = Technician.find_by_email(tech_email)
                    if technician:
                        self.active_user = technician
                        self._technician_actions()
                    else:
                        print("Technician account not found.")
                elif selection == '3':
                    customer_email = input("Enter your registered email: ")
                    customer = Customer.find_by_email(customer_email)
                    if customer:
                        self.active_user = customer
                        self._customer_interactions()
                    else:
                        print("Customer not found. Please proceed as a walk-in.")
                elif selection == '4':
                    self._run_module_tests()
                elif selection == '5':
                    print("Exiting Tech Solutions Portal. Goodbye!")
                    sys.exit()
                else:
                    print("Invalid selection. Please try again.")
            except KeyboardInterrupt:
                print("\n[!] Returning to the main menu.")

    def _admin_operations(self):
        while True:
            try:
                print("\n--- Administrator Console ---")
                actions = {
                    "1": "Register New Customer",
                    "2": "View All Service Requests",
                    "3": "Assign Request to Technician",
                    "4": "Add New Technician Account",
                    "5": "Review Completed Requests & Finalize Cost",
                    "6": "Manage Parts Suppliers",
                    "7": "Logout from Admin Console"
                }
                for key, value in actions.items():
                    print(f"{key}. {value}")
                task = input("Choose an administrative task: ")
                if task == '1':
                    self._register_new_customer()
                elif task == '2':
                    self._view_all_service_requests()
                elif task == '3':
                    self._assign_request_to_technician()
                elif task == '4':
                    self._create_technician_account()
                elif task == '5':
                    self._review_completed_requests_add_cost()
                elif task == '6':
                    self._manage_parts_suppliers()
                elif task == '7':
                    break
                else:
                    print("Invalid task selection.")
            except KeyboardInterrupt:
                print("\n[!] Returning to administrator console.")
                break

    def _remove_parts_suppliers(self):
        supplier_ids_input = input("Enter IDs of suppliers to remove (comma-separated): ")
        try:
            supplier_ids = [int(i.strip()) for i in supplier_ids_input.split(",") if i.strip().isdigit()]
            Supplier.remove_suppliers_by_ids(supplier_ids)
            print("Selected suppliers have been removed.")
        except Exception as e:
            print(f"Error encountered while removing suppliers: {e}")

    def _manage_parts_suppliers(self):
        try:
            print("\n--- Parts Supplier Management ---")
            supplier_options = {
                "1": "Add New Supplier",
                "2": "List All Suppliers",
                "3": "Remove Suppliers"
            }
            for key, value in supplier_options.items():
                print(f"{key}. {value}")
            supplier_choice = input("Select supplier action: ")

            if supplier_choice == '1':
                supplier_name = input("Enter supplier's name: ")
                part_category = input("Enter type of parts supplied: ")
                supplier_location = input("Enter supplier's location: ")
                new_supplier = Supplier(supplier_name, part_category, supplier_location)
                new_supplier.save()
                print(f"Supplier '{supplier_name}' added successfully.")
            elif supplier_choice == '2':
                suppliers_list = Supplier.get_all()
                if suppliers_list:
                    for supplier in suppliers_list:
                        print(f"ID: {supplier[0]}, Name: {supplier[1]}, Parts: {supplier[2]}, Location: {supplier[3]}")
                else:
                    print("No suppliers currently listed.")
            elif supplier_choice == '3':
                self._remove_parts_suppliers()
            else:
                print("Invalid supplier option.")
        except Exception as e:
            print(f"[!] An error occurred: {e}")

    def _create_technician_account(self):
        try:
            tech_name = input("Enter technician's full name: ")
            tech_email = input("Enter technician's email address: ")
            tech_expertise = input("Enter technician's area of expertise: ")
            new_technician = Technician(tech_name, tech_email, tech_expertise)
            new_technician.save()
            print(f"Technician '{tech_name}' with email '{tech_email}' has been added.")
        except Exception as e:
            print(f"[!] Error creating technician account: {e}")

    def _register_new_customer(self):
        try:
            customer_name = input("Enter customer's name: ")
            customer_email = input("Enter customer's email: ")
            equipment_type = input("Enter equipment make/type: ")
            serial_number = input("Enter equipment serial number: ")

            new_customer = Customer(customer_name, customer_email)
            customer_id = new_customer.save()
            new_equipment = Equipment(customer_id, equipment_type, serial_number)
            new_equipment.save()
            print(f"Customer '{customer_name}' and equipment details recorded.")
        except Exception as e:
            print(f"Error during customer registration: {e}")

    def _view_all_service_requests(self):
        all_jobs = Job.get_all()
        if all_jobs:
            for job_details in all_jobs:
                print(f"Request ID: {job_details[0]}, Customer: {job_details[6]}, Issue: {job_details[3]}, Status: {job_details[4]}, Estimated Cost: {job_details[5]}")
        else:
            print("No service requests currently in the system.")

    def _assign_request_to_technician(self):
        try:
            device_id = input("Enter Equipment ID for the service request: ")
            tech_id = input("Enter Technician ID to assign: ")
            issue_description = input("Enter a brief description of the issue: ")
            new_job = Job(issue_description, technician_id=tech_id, equipment_id=device_id)
            new_job.save()
            print(f"Service request created with ID: {new_job.id}")
        except Exception as e:
            print(f"Error assigning service request: {e}")

    def _technician_actions(self):
        while True:
            try:
                print("\n--- Technician Interface ---")
                tech_options = {
                    "1": "View My Assigned Service Requests",
                    "2": "Update Status of Service Request",
                    "3": "Manage Parts Suppliers",
                    "4": "Logout from Technician Interface"
                }
                for key, value in tech_options.items():
                    print(f"{key}. {value}")
                tech_choice = input("Select an action: ")
                if tech_choice == '1':
                    self._view_assigned_service_requests()
                elif tech_choice == '2':
                    self._update_service_request_status()
                elif tech_choice == '3':
                    self._manage_parts_suppliers()
                elif tech_choice == '4':
                    break
                else:
                    print("Invalid selection.")
            except KeyboardInterrupt:
                print("\n[!] Returning to technician interface.")
                break

    def _view_assigned_service_requests(self):
        try:
            technician_identifier = self.active_user.get_id()
            assigned_jobs = Job.get_by_technician(technician_identifier)
            if assigned_jobs:
                for job_info in assigned_jobs:
                    print(f"\nRequest ID: {job_info[0]}, Issue: {job_info[1]}, Status: {job_info[2]}")
                    print(f"  Equipment: {job_info[3]}, Serial: {job_info[4]}")
            else:
                print("No service requests currently assigned to you.")
        except Exception as e:
            print(f"Error retrieving assigned jobs: {e}")

    def _update_service_request_status(self):
        request_ids = input("Enter Request IDs to mark as 'Assessed' (comma-separated): ")
        try:
            job_identifiers = [int(x.strip()) for x in request_ids.split(",") if x.strip().isdigit()]
            if Job.update_status_for_technician(job_identifiers, self.active_user.id):
                print("Status of selected service requests updated to 'Assessed'.")
        except ValueError:
            print("Invalid input. Please enter numeric Request IDs separated by commas.")

    def _customer_interactions(self):
        while True:
            try:
                print("\n--- Customer Portal ---")
                customer_options = {
                    "1": "Submit Equipment for Repair",
                    "2": "Logout from Customer Portal"
                }
                for key, value in customer_options.items():
                    print(f"{key}. {value}")
                customer_choice = input("Select an option: ")
                if customer_choice == '1':
                    self._submit_equipment_for_repair()
                elif customer_choice == '2':
                    break
                else:
                    print("Invalid choice.")
            except KeyboardInterrupt:
                print("\n[!] Returning to customer portal.")
                break

    def _submit_equipment_for_repair(self):
        try:
            device_type = input("Enter equipment type: ")
            device_serial = input("Enter serial number: ")
            customer_identifier = self.active_user.get_id()
            equipment_record = Equipment(customer_identifier, device_type, device_serial)
            equipment_record.save(customer_identifier, device_type, device_serial)
            print("Equipment details submitted for repair.")
        except Exception as e:
            print(f"Error submitting equipment for repair: {e}")

    def _review_completed_requests_add_cost(self):
        try:
            completed_jobs = Job.get_assessed_jobs()
            if not completed_jobs:
                print("No assessed service requests found.")
                return

            print("\n--- Assessed Service Requests ---")
            for job_details in completed_jobs:
                cost_info = f", Final Cost: {job_details[5]}" if len(job_details) > 5 else ", Cost: Not Yet Added"
                print(f"Request ID: {job_details[0]}, Equipment ID: {job_details[1]}, Technician ID: {job_details[2]}, Issue: {job_details[3]}, Status: {job_details[4]}{cost_info}")

            selected_job_id = input("Enter Request ID to add final cost (or press Enter to skip): ").strip()
            if selected_job_id:
                final_cost = input("Enter the final cost amount: ").strip()
                Job.update_cost(int(selected_job_id), float(final_cost))
                print("Final cost updated for the selected request.")
        except Exception as e:
            print(f"[!] Error processing assessed jobs: {e}")

    def _run_module_tests(self):
        """Locates and executes unit tests within the 'tests' directory."""
        print("\n--- Executing Unit Tests ---")
        tests_directory = os.path.join(os.path.dirname(__file__), '..', 'tests')
        if not os.path.isdir(tests_directory):
            tests_directory = os.path.join(os.path.dirname(__file__), 'tests')

        if not os.path.isdir(tests_directory):
            print(f"Error: Test directory not found at expected paths.")
            print(f"Searched in: {os.path.join(os.path.dirname(__file__), '..', 'tests')} and {os.path.join(os.path.dirname(__file__), 'tests')}")
            return

        print(f"Discovering test modules in: {tests_directory}")
        test_loader = unittest.TestLoader()
        test_suite = test_loader.discover(tests_directory, pattern='test_*.py')

        if test_suite.countTestCases() == 0:
            print("No test cases found.")
            return

        test_runner = unittest.TextTestRunner(verbosity=2)
        test_results = test_runner.run(test_suite)

        print("--- Test Execution Completed ---")
        if test_results.wasSuccessful():
            print("All test cases passed successfully!")
        else:
            print("Some test cases failed.")
        input("Press Enter to return to the main application...")

if __name__ == "__main__":
    app = ServiceHub()
    app.initiate_session()