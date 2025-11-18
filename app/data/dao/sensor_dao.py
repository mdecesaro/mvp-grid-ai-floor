from app.data.models.sensor import Sensor

class SensorDAO:
    def __init__(self, db_manager):
        self.db = db_manager
        
    def get_all_sensors(self, layout="pro"):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM sensors WHERE layout = ? ORDER BY id", (layout,))
        rows = cursor.fetchall()
        return [Sensor(**dict(row)) for row in rows]

    def get_sensor_by_id(self, layout, sensor_id):
        print(layout, sensor_id)
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM sensors WHERE layout = ? AND sensor = ?",(layout, sensor_id,))
        row = cursor.fetchone()
        return Sensor(**dict(row)) if row else None
