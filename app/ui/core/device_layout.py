from app.config.config import GRIDAI_PRO_IMAGE_PATH, GRIDAI_HOME_IMAGE_PATH

class DeviceLayout:
    def __init__(self, sensor_count=0, sensor_dao=None):
        self.sensor_count = sensor_count
        self.type = None
        self.layout = []
        self.excluded_sensors = set()
        self.sensors = []
        self.layout_image = None
        self.thumbnail_image = []
        self.image_x = None
        self.image_y = None
        
        self.sensor_dao = sensor_dao
        if sensor_count and sensor_dao:
            self.load_layout(sensor_count)

    def load_layout(self, sensor_count):
        self.sensor_count = sensor_count
        if self.sensor_count == 32:
            self.type = "pro"
            self.layout_image = GRIDAI_PRO_IMAGE_PATH
            self.thumbnail_image = (670, 643)
            self.image_x = 80
            self.image_y = 50
            self.layout = [4, 5, 6, 7, 6, 5, 4]
            self.excluded_sensors = {11, 12, 18, 24, 25}
        elif self.sensor_count == 14:
            self.type = "home"
            self.layout_image = GRIDAI_HOME_IMAGE_PATH
            self.thumbnail_image = (687, 704)
            self.image_x = 60
            self.image_y = 20
            self.layout = [3, 4, 5, 4, 3]
            self.excluded_sensors = {4, 5, 9, 13, 14}
        else:
            self.type = None
            self.layout_image = None
            self.thumbnail_image = []
            self.image_x = None
            self.image_y = None 
            self.layout = []
            self.excluded_sensors = set()

        if self.sensor_count > 0 and self.type is not None:
            self.sensors = self.sensor_dao.get_all_sensors(self.type)
        else:
            self.sensors = []
        
    def is_layout_drawable(self):
        if self.sensor_count > 0:
            return True
        else:
            return False

    def get_sensor(self, sensor_number):
        for s in self.sensors:
            if s.sensor == sensor_number:
                return s
        return None

    def is_sensor_excluded(self, sensor_number):
        return sensor_number in self.excluded_sensors

    def __repr__(self):
        return f"<DeviceLayout type={self.type} sensors={len(self.sensors)}>"

