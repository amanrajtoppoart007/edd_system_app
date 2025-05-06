from app.models.user import User
from app.models.roles import Roles
from app.models.customer import Customer
from app.models.equipment import Equipment

class Administrator(User):
    def __init__(self, name):
        super().__init__(name, Roles.ADMIN)

    def register_walkin_customer(self):
        name = input("Enter customer name: ")
        email = input("Enter email: ")
        equipment_type = input("Enter equipment type: ")
        serial = input("Enter serial number: ")
        customer = Customer(name, email)
        customer_id = customer.save()
        Equipment.save(customer_id, equipment_type, serial)
        print("Walk-in customer and equipment recorded successfully.")
