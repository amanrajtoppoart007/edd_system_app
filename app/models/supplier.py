from app.database.db import Database

class Supplier:
    def __init__(self, name, part_type, location, id=None):
        self.id = id
        self.name = name
        self.part_type = part_type
        self.location = location

    def save(self):
        db = Database().get_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO suppliers (name, part_type, location) VALUES (?, ?, ?)",
            (self.name, self.part_type, self.location)
        )
        db.commit()
        self.id = cursor.lastrowid
        return self.id

    @staticmethod
    def get_all():
        db = Database().get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM suppliers")
        return cursor.fetchall()
    
    @staticmethod
    def remove_suppliers_by_ids(id_list):
        db = Database().get_connection()
        cursor = db.cursor()
        cursor.executemany("DELETE FROM suppliers WHERE id = ?", [(i,) for i in id_list])
        db.commit()