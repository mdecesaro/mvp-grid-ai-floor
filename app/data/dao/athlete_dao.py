from app.data.models.athlete import Athlete

class AthleteDAO:
    def __init__(self, db_manager):
        self.db = db_manager

    def insert_athlete(self, name, gender, country, birth, dominant_foot, position, profile):
        cursor = self.db.get_cursor()
        cursor.execute("""
            INSERT INTO athletes (name, gender, country, birth, dominant_foot, position, profile)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (name, gender, country, birth, dominant_foot, position, profile))
        self.db.commit()
        return cursor.lastrowid  
    
    def get_all_athletes(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT id, name, gender, country, birth, dominant_foot, position, profile FROM athletes")
        rows = cursor.fetchall()
        return [Athlete.from_row(row) for row in rows]

    def get_athlete_by_id(self, athlete_id):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT id,name,gender,country,birth,dominant_foot,position,profile FROM athletes WHERE id = ?", (athlete_id,))
        row = cursor.fetchone()
        return Athlete.from_row(row) if row else None
