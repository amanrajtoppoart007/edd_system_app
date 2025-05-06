# services/supplier_manager.py
class SupplierManager:
    def __init__(self):
        self.suppliers = []

    def add_supplier(self, name, location):
        self.suppliers.append({"name": name, "location": location})

    def list_suppliers(self):
        return self.suppliers