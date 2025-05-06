from app.db.db import DB

class Customer:
    def __init__(self, name, email, id=None):
        self.name = name
        self.email = email
        self.id = id

    def save(self):
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO customers (name, email) VALUES (?, ?)", (self.name, self.email))
        db.commit()
        self.id = cursor.lastrowid
        return self.id
    
    @staticmethod
    def get_all():
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM customers")
        return cursor.fetchall()

    @staticmethod
    def find_by_email(email):
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, name, email FROM customers WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return Customer(row[1], row[2], id=row[0])
        return None

    def get_id(self):
        return self.id