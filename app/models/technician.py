from app.database.db import Database

class Technician:
    def __init__(self, name=None, email=None, expertise=None, id=None):
        self.id = id
        self.name = name
        self.email = email
        self.expertise = expertise

    def save(self):
        db = Database().get_connection()
        cursor = db.cursor()
        cursor.execute("INSERT INTO technicians (name, email, expertise) VALUES (?, ?, ?)",
                       (self.name, self.email, self.expertise))
        db.commit()
        self.id = cursor.lastrowid
        return self.id
    
    def get_id(self):
            return self.id
    
    @staticmethod
    def find_by_email(email):
        db = Database().get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT id, name, email, expertise FROM technicians WHERE email = ?", (email,))
        row = cursor.fetchone()
        if row:
            return Technician(name=row[1], email=row[2], expertise=row[3], id=row[0])
        return None
    
    @staticmethod
    def get_all():
        db = Database().get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM technicians")
        return cursor.fetchall()
