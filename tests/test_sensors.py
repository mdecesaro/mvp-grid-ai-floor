from app.data.db_manager import DatabaseManager
from app.data.dao.sensor_dao import SensorDAO
from app.data.models.sensor import Sensor

def run_tests():
    print("Running sensors SELECT tests...")

    db = DatabaseManager("app/data/database/plataform.db") 
    sensor_dao = SensorDAO(db)

    # Test 1: Get all Sensors
    print("\n▶️ - All Sensors:")
    sensors = sensor_dao.get_all_sensors("home")
    print(sensors)
    for s in sensors:
        print(f"Sensor {s.sensor}: {s.neighbors}")
    
    # Test 2: Get sensor by ID
    print("\n▶️ - Get sensor by ID:")
    sensor = sensor_dao.get_sensor_by_id("home", 2)
    print(f"Sensor {sensor.sensor}: {sensor.neighbors}")

if __name__ == "__main__":
    run_tests()

#python3 -m tests.test_sensors