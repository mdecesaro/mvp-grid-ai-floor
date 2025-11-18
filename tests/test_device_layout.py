from app.data.db_manager import DatabaseManager
from app.data.dao.sensor_dao import SensorDAO
from app.ui.core.device_layout import DeviceLayout

def run_tests():
    print("Running category and subcategory SELECT tests...")

    db = DatabaseManager("app/data/database/plataform.db")  
    sensorDAO = SensorDAO(db)
    device_layout = DeviceLayout(sensor_dao=sensorDAO)
    device_layout.load_layout(14)
    
    print(device_layout.layout)
    print(device_layout.excluded_sensors)
    print(device_layout.sensors)

if __name__ == "__main__":
    run_tests()



#python3 -m tests.test_device_layout