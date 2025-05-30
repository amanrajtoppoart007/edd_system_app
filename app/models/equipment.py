from app.db.db import DB

class Equipment:
    def __init__(self, customer_id, type=None, serial_number=None, id=None):
        self.customer_id = customer_id
        self.type = type
        self.serial_number = serial_number
        self.id = id

    def save(self):
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO equipment (customer_id, type, serial_number) VALUES (?, ?, ?)",
            (self.customer_id, self.type, self.serial_number)
        )
        db.commit()
        self.id = cursor.lastrowid
        return self.id

    @staticmethod
    def get_by_customer(customer_id):
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute(
            "SELECT id, type, serial_number FROM equipment WHERE customer_id = ?",
            (customer_id,)
        )
        return cursor.fetchall()
