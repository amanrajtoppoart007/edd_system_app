import sys
import unittest
import os

# Attempt to import necessary project modules.
# These modules are essential for the application's core functionality.
try:
    from app.models.customer import Customer
    from app.models.equipment import Equipment
    from app.models.job import Job
    from app.models.administrator import Administrator
    from app.models.technician import Technician
    from app.db.db import DB
    from app.models.supplier import Supplier
except ImportError as e:
    # If critical modules are missing, the application cannot proceed.
    # Log this critical error and exit.
    print(f"[CRITICAL ERROR] Essential application modules failed to import: {e}")
    print("Please ensure all 'app.models' and 'app.db' modules are correctly installed and accessible.")
    print("The application will now terminate.")
    sys.exit(1) # Exit with an error code


class AppAction:
    def __init__(self):
        self.active_user = None
        try:
            # Initialize the database connection.
            self.data_store = DB()
        except Exception as e:
            print(f"[CRITICAL ERROR] Failed to initialize database connection: {e}")
            sys.exit("Application cannot start without a database connection.")

    def start(self):
        """Main application loop to present user options and handle selections."""
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

                selection = input("Select an action: ").strip()
                if not selection:
                    print("No input provided. Please select an option.")
                    continue

                if selection == '1':
                    admin_name = input("Enter administrator username: ").strip()
                    if not admin_name:
                        print("Administrator username cannot be empty.")
                        continue
                    # Administrator object is instantiated.
                    self.active_user = Administrator(admin_name)
                    self._admin_operations()
                elif selection == '2':
                    tech_email = input("Enter technician email address: ").strip()
                    if not tech_email:
                        print("Technician email cannot be empty.")
                        continue
                    try:
                        # Attempt to find technician by email via the Technician model.
                        technician = Technician.find_by_email(tech_email)
                        if technician:
                            self.active_user = technician
                            self._technician_actions()
                        else:
                            print("Technician account not found with that email.")
                    except Exception as e:
                        print(f"[ERROR] Could not retrieve technician information: {e}")
                elif selection == '3':
                    customer_email = input("Enter your registered email: ").strip()
                    if not customer_email:
                        print("Customer email cannot be empty.")
                        continue
                    try:
                        # Attempt to find customer by email via the Customer model.
                        customer = Customer.find_by_email(customer_email)
                        if customer:
                            self.active_user = customer
                            self._customer_interactions()
                        else:
                            print("Customer not found. If you are new, an admin can register you.")
                    except Exception as e:
                        print(f"[ERROR] Could not retrieve customer information: {e}")
                elif selection == '4':
                    self._run_module_tests()
                elif selection == '5':
                    print("Exiting Tech Solutions Portal. Goodbye!")
                    sys.exit()
                else:
                    print("Invalid selection. Please enter a number from the options.")
            except KeyboardInterrupt:
                print("\nAction interrupted. Returning to the main menu.")
            except EOFError: # Handle Ctrl+D for graceful exit.
                print("\nEOF signal received. Exiting application.")
                sys.exit()
            except Exception as e:
                print(f"[CRITICAL ERROR] An unexpected error occurred in the main application loop: {e}")
                # Further error logging or specific recovery logic could be added here.

    def _admin_operations(self):
        """Handles operations available to an administrator."""
        if not isinstance(self.active_user, Administrator):
            print("[ERROR] No administrator logged in or invalid session. Returning to main menu.")
            return

        while True:
            try:
                print(f"\n--- Administrator Console (Logged in as: {self.active_user.name}) ---")
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

                task = input("Choose an administrative task: ").strip()
                if not task:
                    print("No task selected. Please choose an option.")
                    continue

                if task == '1': self._register_new_customer()
                elif task == '2': self._view_all_service_requests()
                elif task == '3': self._assign_request_to_technician()
                elif task == '4': self._create_technician_account()
                elif task == '5': self._review_completed_requests_add_cost()
                elif task == '6': self._manage_parts_suppliers()
                elif task == '7':
                    print("Logging out from Admin Console.")
                    self.active_user = None # Clear active user session on logout.
                    break
                else:
                    print("Invalid task selection. Please enter a number from the options.")
            except KeyboardInterrupt:
                print("\nAction interrupted. Returning to administrator console menu.")
            except EOFError:
                print("\nEOF signal received. Logging out and returning to main menu.")
                self.active_user = None
                break
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred in administrator operations: {e}")

    def _remove_parts_suppliers(self):
        """Handles removal of parts suppliers by their IDs."""
        supplier_ids_input = input("Enter IDs of suppliers to remove (comma-separated, e.g., 1,2,3): ").strip()
        if not supplier_ids_input:
            print("No supplier IDs provided for removal.")
            return
        try:
            supplier_ids_to_remove = []
            for item in supplier_ids_input.split(","):
                item_stripped = item.strip()
                if item_stripped.isdigit():
                    supplier_ids_to_remove.append(int(item_stripped))
                elif item_stripped: # Handles non-empty, non-digit strings.
                    print(f"Warning: '{item_stripped}' is not a valid ID format and will be ignored.")

            if not supplier_ids_to_remove:
                print("No valid supplier IDs were entered for removal.")
                return

            # Delegate removal to the Supplier model.
            Supplier.remove_suppliers_by_ids(supplier_ids_to_remove)
            print(f"Attempted to remove suppliers with IDs: {supplier_ids_to_remove}. Check system logs for details.")
        except ValueError:
            print("[ERROR] Invalid input format for supplier IDs. Please use comma-separated numbers.")
        except Exception as e:
            print(f"[ERROR] Encountered an issue while removing suppliers: {e}")

    def _manage_parts_suppliers(self):
        """Provides interface for managing parts suppliers (add, list, remove)."""
        while True:
            try:
                print("\n--- Parts Supplier Management ---")
                supplier_options = {
                    "1": "Add New Supplier",
                    "2": "List All Suppliers",
                    "3": "Remove Suppliers",
                    "4": "Back to Admin Menu"
                }
                for key, value in supplier_options.items():
                    print(f"{key}. {value}")
                supplier_choice = input("Select supplier action: ").strip()

                if supplier_choice == '1':
                    supplier_name = input("Enter supplier's name: ").strip()
                    part_category = input("Enter type of parts supplied: ").strip()
                    supplier_location = input("Enter supplier's location: ").strip()

                    if not all([supplier_name, part_category, supplier_location]):
                        print("[ERROR] All supplier fields (name, category, location) are mandatory.")
                        continue
                    
                    new_supplier = Supplier(supplier_name, part_category, supplier_location)
                    new_supplier.save() # Supplier model's save method is called.
                    print(f"Supplier '{supplier_name}' added successfully.")

                elif supplier_choice == '2':
                    suppliers_list = Supplier.get_all()
                    if suppliers_list:
                        print("\n--- Current Suppliers ---")
                        for supplier_data in suppliers_list: # Iterates over supplier data tuples/objects.
                            print(f"ID: {supplier_data[0]}, Name: {supplier_data[1]}, Parts: {supplier_data[2]}, Location: {supplier_data[3]}")
                        print("--- End of List ---")
                    else:
                        print("No suppliers are currently listed in the system.")
                elif supplier_choice == '3':
                    self._remove_parts_suppliers()
                elif supplier_choice == '4':
                    break # Exit supplier management and return to admin menu.
                else:
                    print("Invalid supplier option. Please select a number from the menu.")
            except KeyboardInterrupt:
                print("\nAction interrupted. Returning to supplier management menu.")
            except EOFError:
                print("\nEOF signal received. Returning to admin menu.")
                break
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred in supplier management: {e}")


    def _create_technician_account(self):
        """Handles the creation of a new technician account."""
        try:
            tech_name = input("Enter technician's full name: ").strip()
            tech_email = input("Enter technician's email address: ").strip()
            tech_expertise = input("Enter technician's area of expertise: ").strip()

            if not all([tech_name, tech_email, tech_expertise]):
                print("[ERROR] All technician fields (name, email, expertise) are mandatory.")
                return

            # Basic email format validation.
            if "@" not in tech_email or "." not in tech_email.split('@')[-1]:
                print("[ERROR] Invalid email format provided for technician.")
                return

            new_technician = Technician(tech_name, tech_email, tech_expertise)
            new_technician.save() # Technician model's save method is called.
            print(f"Technician account for '{tech_name}' with email '{tech_email}' has been created successfully.")
        except Exception as e:
            # Catches potential errors from model interaction or other issues.
            print(f"[ERROR] Failed to create technician account: {e}")

    def _register_new_customer(self):
        """Handles the registration of a new customer and their equipment."""
        try:
            customer_name = input("Enter customer's name: ").strip()
            customer_email = input("Enter customer's email: ").strip()
            equipment_type = input("Enter equipment make/type (e.g., Laptop, Phone): ").strip()
            serial_number = input("Enter equipment serial number: ").strip()

            if not all([customer_name, customer_email, equipment_type, serial_number]):
                print("[ERROR] All fields (name, email, equipment type, serial number) are mandatory.")
                return
            
            if "@" not in customer_email or "." not in customer_email.split('@')[-1]:
                print("[ERROR] Invalid customer email format provided.")
                return

            # It is good practice to check if a customer with this email already exists.
            # This logic would typically be in the Customer model or a service layer.
            new_customer = Customer(customer_name, customer_email)
            customer_id = new_customer.save() # Customer model's save method, returns ID.
            
            if customer_id: # Confirms customer was saved.
                new_equipment = Equipment(customer_id, equipment_type, serial_number)
                new_equipment.save() # Equipment model's save method.
                print(f"Customer '{customer_name}' and their equipment '{equipment_type}' registered successfully.")
            else:
                print("[ERROR] Failed to save new customer profile. Equipment registration aborted.")

        except Exception as e:
            print(f"[ERROR] An error occurred during customer registration: {e}")

    def _view_all_service_requests(self):
        """Displays all service requests currently in the system."""
        try:
            all_jobs = Job.get_all()
            if all_jobs:
                print("\n--- All Service Requests ---")
                for job_details in all_jobs: # Iterates over job data.
                    # Defensive access to tuple/list elements.
                    job_id = job_details[0] if len(job_details) > 0 else "N/A"
                    customer_name = job_details[6] if len(job_details) > 6 else "N/A" # Example index
                    issue = job_details[3] if len(job_details) > 3 else "N/A" # Example index
                    status = job_details[4] if len(job_details) > 4 else "N/A" # Example index
                    cost = job_details[5] if len(job_details) > 5 else "Not set" # Example index
                    print(f"Request ID: {job_id}, Customer: {customer_name}, Issue: {issue}, Status: {status}, Estimated Cost: {cost}")
                print("--- End of List ---")
            else:
                print("No service requests are currently in the system.")
        except Exception as e:
            print(f"[ERROR] Could not retrieve service requests: {e}")

    def _assign_request_to_technician(self):
        """Assigns a service request (Job) to a technician."""
        try:
            device_id_str = input("Enter Equipment ID for the service request: ").strip()
            tech_id_str = input("Enter Technician ID to assign: ").strip()
            issue_description = input("Enter a brief description of the issue: ").strip()

            if not all([device_id_str, tech_id_str, issue_description]):
                print("[ERROR] Equipment ID, Technician ID, and issue description are all mandatory.")
                return

            try:
                device_id = int(device_id_str)
                tech_id = int(tech_id_str)
            except ValueError:
                print("[ERROR] Equipment ID and Technician ID must be valid numbers.")
                return

            # Validations for existence of Equipment ID and Technician ID should be performed,
            # ideally before creating the Job object or within the Job model's save logic.
            new_job = Job(description=issue_description, technician_id=tech_id, equipment_id=device_id)
            job_id = new_job.save() # Job model's save method, returns new job ID.
            if job_id:
                print(f"Service request created successfully with ID: {job_id} and assigned to Technician ID: {tech_id}.")
            else:
                print("[ERROR] Failed to create and assign service request. Please verify details.")
        except Exception as e:
            print(f"[ERROR] An error occurred while assigning the service request: {e}")

    def _technician_actions(self):
        """Handles operations available to a logged-in technician."""
        if not self.active_user or not hasattr(self.active_user, 'email'): # Verifies active user is a technician.
            print("[ERROR] No technician logged in or invalid session. Returning to main menu.")
            return

        while True:
            try:
                print(f"\n--- Technician Interface (Logged in as: {self.active_user.email}) ---")
                tech_options = {
                    "1": "View My Assigned Service Requests",
                    "2": "Update Status of Service Request",
                    "3": "Logout from Technician Interface"
                }
                for key, value in tech_options.items():
                    print(f"{key}. {value}")
                
                tech_choice = input("Select an action: ").strip()
                if not tech_choice:
                    print("No action selected. Please choose an option.")
                    continue

                if tech_choice == '1':
                    self._view_assigned_service_requests()
                elif tech_choice == '2':
                    self._update_service_request_status()
                elif tech_choice == '3':
                    print("Logging out from Technician Interface.")
                    self.active_user = None # Clear active user session.
                    break
                else:
                    print("Invalid selection. Please enter a number from the options.")
            except KeyboardInterrupt:
                print("\nAction interrupted. Returning to technician interface menu.")
            except EOFError:
                print("\nEOF signal received. Logging out and returning to main menu.")
                self.active_user = None
                break
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred in technician actions: {e}")


    def _view_assigned_service_requests(self):
        """Displays service requests assigned to the currently logged-in technician."""
        if not self.active_user or not hasattr(self.active_user, 'get_id'):
            print("[ERROR] Cannot retrieve jobs: No active technician user session.")
            return
        try:
            technician_identifier = self.active_user.get_id() # Retrieves ID from active user object.
            assigned_jobs = Job.get_by_technician(technician_identifier)
            if assigned_jobs:
                print("\n--- Your Assigned Service Requests ---")
                for job_info in assigned_jobs: # Iterates over job data.
                    job_id = job_info[0] if len(job_info) > 0 else "N/A"
                    issue = job_info[1] if len(job_info) > 1 else "N/A"
                    status = job_info[2] if len(job_info) > 2 else "N/A"
                    equipment_type = job_info[3] if len(job_info) > 3 else "N/A"
                    serial_num = job_info[4] if len(job_info) > 4 else "N/A"
                    print(f"\nRequest ID: {job_id}, Issue: {issue}, Status: {status}")
                    print(f"  Equipment: {equipment_type}, Serial: {serial_num}")
                print("--- End of List ---")
            else:
                print("No service requests are currently assigned to you.")
        except AttributeError: 
             print("[ERROR] Internal system error: Active user object is not correctly configured for ID retrieval.")
        except Exception as e:
            print(f"[ERROR] Failed to retrieve assigned service requests: {e}")

    def _update_service_request_status(self):
        """Allows a technician to update the status of one or more service requests."""
        if not self.active_user or not hasattr(self.active_user, 'get_id'):
            print("[ERROR] Cannot update status: No active technician user session.")
            return

        request_ids_input = input("Enter Request IDs to mark as 'Assessed' (comma-separated, e.g., 1,2,3): ").strip()
        if not request_ids_input:
            print("No Request IDs provided for status update.")
            return
        
        try:
            job_identifiers_to_update = []
            for x_str in request_ids_input.split(","):
                x_stripped = x_str.strip()
                if x_stripped.isdigit():
                    job_identifiers_to_update.append(int(x_stripped))
                elif x_stripped:
                    print(f"Warning: '{x_stripped}' is not a valid ID format and will be ignored.")
            
            if not job_identifiers_to_update:
                print("No valid numeric Request IDs were entered.")
                return

            technician_id = self.active_user.get_id()
            # Job model's method to update status for specific jobs by a technician.
            success = Job.update_status_for_technician(job_identifiers_to_update, technician_id)
            if success: 
                print(f"Status of service requests {job_identifiers_to_update} updated to 'Assessed'.")
            else:
                print("Failed to update status for some or all selected requests. They may not exist or are not assigned to you.")
        except ValueError: 
            print("[ERROR] Invalid input. Please enter numeric Request IDs separated by commas.")
        except AttributeError:
             print("[ERROR] Internal system error: Active user object not configured for ID retrieval.")
        except Exception as e:
            print(f"[ERROR] An error occurred while updating service request status: {e}")

    def _customer_interactions(self):
        """Handles operations available to a logged-in customer."""
        if not self.active_user or not hasattr(self.active_user, 'email'): # Verifies active user is a customer.
            print("[ERROR] No customer logged in or invalid session. Returning to main menu.")
            return
        
        while True:
            try:
                print(f"\n--- Customer Portal (Logged in as: {self.active_user.email}) ---")
                customer_options = {
                    "1": "Submit Equipment for Repair",
                    "2": "View My Repair Job Statuses (Feature Coming Soon)", 
                    "3": "Logout from Customer Portal"
                }
                for key, value in customer_options.items():
                    print(f"{key}. {value}")
                
                customer_choice = input("Select an option: ").strip()
                if not customer_choice:
                    print("No option selected.")
                    continue

                if customer_choice == '1':
                    self._submit_equipment_for_repair()
                elif customer_choice == '2':
                    print("This feature is currently under development. Please check back later.")
                elif customer_choice == '3':
                    print("Logging out from Customer Portal.")
                    self.active_user = None # Clear active user session.
                    break
                else:
                    print("Invalid choice. Please select a number from the options.")
            except KeyboardInterrupt:
                print("\nAction interrupted. Returning to customer portal menu.")
            except EOFError:
                print("\nEOF signal received. Logging out and returning to main menu.")
                self.active_user = None
                break
            except Exception as e:
                print(f"[ERROR] An unexpected error occurred in the customer portal: {e}")

    def _submit_equipment_for_repair(self):
        """Allows a customer to submit their equipment for repair."""
        if not self.active_user or not hasattr(self.active_user, 'get_id'):
            print("[ERROR] Cannot submit equipment: No active customer user session.")
            return
        try:
            device_type = input("Enter equipment type (e.g., Laptop, Smartphone): ").strip()
            device_serial = input("Enter serial number: ").strip()

            if not all([device_type, device_serial]):
                print("[ERROR] Equipment type and serial number are both mandatory.")
                return

            customer_identifier = self.active_user.get_id()
            # Equipment object is instantiated with customer ID and device details.
            equipment_record = Equipment(customer_id=customer_identifier, type=device_type, serial_number=device_serial)
            equipment_id = equipment_record.save() # Equipment model's save method.

            if equipment_id: 
                print(f"Equipment '{device_type}' (Serial: {device_serial}) submitted successfully for repair.")
                # A new Job should typically be created here or flagged for admin review.
            else:
                print("[ERROR] Failed to submit equipment for repair. Please try again.")
        except AttributeError:
            print("[ERROR] Internal system error: Active customer object not correctly configured.")
        except Exception as e:
            print(f"[ERROR] An error occurred while submitting equipment for repair: {e}")

    def _review_completed_requests_add_cost(self):
        """Allows an administrator to review assessed jobs and add final costs."""
        try:
            # Retrieves jobs that are assessed and may be pending final cost.
            assessed_jobs = Job.get_assessed_jobs()
            if not assessed_jobs:
                print("No service requests are currently marked as 'Assessed' or awaiting final cost.")
                return

            print("\n--- Assessed Service Requests Awaiting Final Cost ---")
            job_dict = {} # Used for quick lookup of a job by its ID.
            for job_details in assessed_jobs:
                job_id = job_details[0] if len(job_details) > 0 else None
                if job_id is None: continue # Skip entry if job_id is missing.

                equipment_id = job_details[1] if len(job_details) > 1 else "N/A"
                tech_id = job_details[2] if len(job_details) > 2 else "N/A"
                issue = job_details[3] if len(job_details) > 3 else "N/A"
                status = job_details[4] if len(job_details) > 4 else "N/A"
                cost = job_details[5] if len(job_details) > 5 and job_details[5] is not None else "Not Yet Added"
                
                job_dict[job_id] = job_details # Store job details for easy access.
                print(f"Request ID: {job_id}, Equipment ID: {equipment_id}, Technician ID: {tech_id}, Issue: {issue}, Status: {status}, Final Cost: {cost}")
            
            if not job_dict: # No valid jobs were processed.
                print("No valid assessed jobs found to process for cost addition.")
                return

            selected_job_id_str = input("Enter Request ID to add/update final cost (or press Enter to skip): ").strip()
            if selected_job_id_str:
                try:
                    selected_job_id = int(selected_job_id_str)
                    if selected_job_id not in job_dict:
                        print(f"Request ID {selected_job_id} not found in the current list of assessed jobs.")
                        return
                except ValueError:
                    print("[ERROR] Invalid Request ID format. Please enter a number.")
                    return

                final_cost_str = input(f"Enter the final cost amount for Request ID {selected_job_id}: ").strip()
                try:
                    final_cost = float(final_cost_str)
                    if final_cost < 0:
                        print("[ERROR] Final cost cannot be a negative value.")
                        return
                    Job.update_cost(selected_job_id, final_cost) # Job model updates cost.
                    print(f"Final cost updated to {final_cost:.2f} for Request ID {selected_job_id}.")
                except ValueError:
                    print("[ERROR] Invalid cost amount. Please enter a numeric value (e.g., 120.50).")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred while processing assessed jobs for cost finalization: {e}")


    def _run_module_tests(self):
        """Locates and executes unit tests within the 'tests' directory."""
        print("\n--- Executing Unit Tests ---")
        
        script_dir = os.path.dirname(__file__) # Directory of the current script.
        # Common project structures:
        # 1. project_root/app_directory/this_script.py and project_root/tests/
        # 2. project_root/this_script.py and project_root/tests/
        project_root_guess1 = os.path.join(script_dir, '..') 
        project_root_guess2 = script_dir 

        tests_directory_path1 = os.path.join(project_root_guess1, 'tests')
        tests_directory_path2 = os.path.join(project_root_guess2, 'tests')

        tests_directory = None
        # Determine the correct tests directory path.
        if os.path.isdir(tests_directory_path1):
            tests_directory = tests_directory_path1
        elif os.path.isdir(tests_directory_path2):
            tests_directory = tests_directory_path2
        
        if not tests_directory:
            print(f"[ERROR] Test directory not found. Expected locations:")
            print(f"  - {os.path.abspath(tests_directory_path1)}")
            print(f"  - {os.path.abspath(tests_directory_path2)}")
            print("Ensure your 'tests' directory is correctly placed relative to the project structure.")
            input("Press Enter to return to the main application...")
            return

        print(f"Discovering test modules in: {os.path.abspath(tests_directory)}")
        
        # Temporarily add project root to sys.path to aid test discovery if needed.
        original_sys_path = list(sys.path)
        project_root_to_add = None
        if tests_directory == tests_directory_path1 and os.path.abspath(project_root_guess1) not in sys.path:
            project_root_to_add = os.path.abspath(project_root_guess1)
        elif tests_directory == tests_directory_path2 and os.path.abspath(project_root_guess2) not in sys.path:
            project_root_to_add = os.path.abspath(project_root_guess2)
        
        if project_root_to_add:
            sys.path.insert(0, project_root_to_add)
            
        try:
            test_loader = unittest.TestLoader()
            test_suite = test_loader.discover(start_dir=tests_directory, pattern='test_*.py')

            if test_suite.countTestCases() == 0:
                print("No test cases found in the 'tests' directory (matching 'test_*.py').")
                print("Ensure test files are named correctly and contain unittest.TestCase classes.")
            else:
                test_runner = unittest.TextTestRunner(verbosity=2)
                test_results = test_runner.run(test_suite)
                print("\n--- Test Execution Summary ---")
                if test_results.wasSuccessful():
                    print("All discovered test cases passed successfully!")
                else:
                    print("Some test cases FAILED or had ERRORS.")
                    print(f"  Tests run: {test_results.testsRun}")
                    print(f"  Failures: {len(test_results.failures)}")
                    print(f"  Errors: {len(test_results.errors)}")
        except ImportError as ie:
            print(f"[ERROR] Failed to import modules during test discovery or execution: {ie}")
            print("This may be due to incorrect project structure or missing __init__.py files in packages.")
        except Exception as e:
            print(f"[ERROR] An unexpected error occurred during test execution: {e}")
        finally:
            # Restore original sys.path.
            if project_root_to_add and project_root_to_add == sys.path[0]:
                sys.path.pop(0)
        
        input("Press Enter to return to the main application...")


if __name__ == "__main__":
    # This block executes if the script is run directly.
    # It's a common practice to configure sys.path here for simpler execution
    # if the project structure requires it, especially for development.
    # For robust deployment, PYTHONPATH or virtual environments are preferred.
    
    # Example: if script is in project/src/ and app modules are in project/app/
    # current_script_dir = os.path.dirname(os.path.abspath(__file__))
    # project_directory = os.path.dirname(current_script_dir) 
    # if project_directory not in sys.path:
    #    sys.path.insert(0, project_directory)

    app_instance = AppAction()
    app_instance.start()