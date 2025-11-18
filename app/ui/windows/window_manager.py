from app.ui.windows.window_newathlete import NewAthleteWindow
from app.ui.windows.exercice_view import ExerciceView
from app.controllers.exercice_controller import ExerciceController
from app.ui.windows.performance_view import PerformanceTestingView
from app.controllers.performance_controller import PerformanceController
from app.ui.windows.analysis_view import AnalysisView
from app.controllers.analysis_controller import AnalysisController

class WindowManager:
    def __init__(self, root, context):
        self.root = root
        self.context = context
        self.windows = {} 

    def _is_window_open(self, key):
        window = self.windows.get(key)
        return window is not None and window.winfo_exists()

    def _focus_window(self, key):
        window = self.windows.get(key)
        if window:
            window.lift()
            window.focus_force()

    def open_new_athlete(self, key):
        if not self._is_window_open(key):
            view = NewAthleteWindow(self.root, self.context)
            view.protocol("WM_DELETE_WINDOW", lambda: self._close_window(key))
            self.windows[key] = {"view": view, "controller": None}
        else:
            self._focus_window(key)
    
    def open_exercice_library(self, key):
        if not self._is_window_open(key):
            view = ExerciceView(self.root, self.context)
            controller = ExerciceController(view, self.context)
            view.set_controller(controller)
            view.build_form()
            view.build_table()

            view.protocol("WM_DELETE_WINDOW", lambda: self._close_window(key))
            self.windows[key] = {"view": view, "controller": controller}
        else:
            self._focus_window(key)

    def open_performance_testing(self, key):
        if not self._is_window_open(key):
            
            view = PerformanceTestingView(self.root)
            controller = PerformanceController(view, self.context)
            view.set_controller(controller)
            view.build_interface()
            controller.load_data()

            view.protocol("WM_DELETE_WINDOW", lambda: self._close_window(key))
            self.windows[key] = {"view": view, "controller": controller}
        else:
            self._focus_window(key)

    def open_evaluation_testing(self, key):
        if not self._is_window_open(key):
            view = AnalysisView(self.root)
            controller = AnalysisController(view, self.context)
            view.set_controller(controller)
            view.build_interface()
            
            view.protocol("WM_DELETE_WINDOW", lambda: self._close_window(key))
            
            self.windows[key] = {"view": view, "controller": controller}
        else:
            self._focus_window(key)

    def _close_window(self, key):
        window = self.windows.get(key)
        if window:
            view = window["view"]
            controller = window["controller"]

            if view and view.winfo_exists():
                view.destroy()

            del controller
            del view

        self.windows.pop(key, None)
