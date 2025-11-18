from app.data.db_manager import DatabaseManager
from app.ui.windows.window_manager import WindowManager
from app.ui.core.device_layout import DeviceLayout
from app.services.execmanager.executor_manager import ExecutorManager
from app.services.pserial.serial_manager import SerialManager
from app.data.dao.athlete_dao import AthleteDAO
from app.data.dao.sensor_dao import SensorDAO
from app.data.dao.exercise_dao import ExerciseDAO
from app.data.dao.category_dao import CategoryDAO
from app.data.dao.evaluation_dao import EvaluationDAO

class AppContext:
    def __init__(self, root, db_path: str):
        self.window_manager = WindowManager(root, self)
        
        self.db_manager = DatabaseManager(db_path)
        self.athlete_dao = AthleteDAO(self.db_manager) 
        self.sensor_dao = SensorDAO(self.db_manager) 
        self.device_layout = DeviceLayout(sensor_dao=self.sensor_dao)
        self.exercise_dao = ExerciseDAO(self.db_manager)
        self.category_dao = CategoryDAO(self.db_manager) 
        self.evaluation_dao = EvaluationDAO(self.db_manager)

        self.executor_manager = None
        self.serial_manager = SerialManager()

        self.hexgrid_widget = None
        self.hexgrid_controller = None

    def set_hexgrid(self, widget, controller):
        self.hexgrid_widget = widget
        self.hexgrid_controller = controller

    def get_hexgrid(self):
        return self.hexgrid_widget, self.hexgrid_controller

    def set_executor(self, executor):
        if not self.executor_manager:
            self.executor_manager = ExecutorManager(executor)
        else:
            self.executor_manager.set_executor(executor)
    
    def clear_executor(self):
        if self.executor_manager:
            self.executor_manager.set_executor(None) 
            self.executor_manager = None  

    def shutdown(self):
        self.db_manager.close()
