from app.db.db import DB

class Job:
    def __init__(self, description, status="Job Created", technician_id=None,equipment_id=None, id=None):
        self.description = description
        self.status = status
        self.technician_id = technician_id
        self.equipment_id = equipment_id
        self.id = id

    def save(self):
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO jobs (description, status, technician_id,equipment_id) VALUES (?, ?, ? ,?)",
            (self.description, self.status, self.technician_id,self.equipment_id)
        )
        db.commit()
        self.id = cursor.lastrowid
        return self.id

    @staticmethod
    def get_all():
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT jobs.* , customers.name  FROM jobs  JOIN equipment ON jobs.equipment_id = equipment.id JOIN customers ON customers.id = equipment.customer_id")
        return cursor.fetchall()

    @staticmethod
    def get_by_technician(technician_id):
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute('''
            SELECT jobs.id, jobs.description, jobs.status, equipment.type, equipment.serial_number
            FROM jobs
            JOIN equipment ON jobs.equipment_id = equipment.id
            WHERE technician_id = ?
        ''', (technician_id,))
        return cursor.fetchall()
    
    @staticmethod
    def update_status_for_technician(job_ids, technician_id, status="Job Assessed"):
        db = DB().get_connection()
        cursor = db.cursor()
        try:
            for job_id in job_ids:
                cursor.execute(
                    "UPDATE jobs SET status = ? WHERE id = ? AND technician_id = ?",
                    (status, job_id, technician_id)
                )
            db.commit()
            return True
        except Exception as e:
            print(f"[!] Error updating jobs: {e}")
            return False
        
    @staticmethod
    def get_assessed_jobs():
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM jobs WHERE status = 'Job Assessed'")
        return cursor.fetchall()

    @staticmethod
    def update_cost(job_id, cost):
        db = DB().get_connection()
        cursor = db.cursor()
        cursor.execute("UPDATE jobs SET job_cost = ? , status = ?  WHERE id = ?", (cost,'Job Completed', job_id))
        db.commit()        
