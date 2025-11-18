from app.ui.widgets.widget_manager import WidgetManager
from app.ui.widgets.statusbar.statusbar_view import StatusBarWidget
from app.ui.widgets.statusbar.statusbar_controller import StatusBarController
from app.ui.widgets.weather.weather_clock_view import WeatherClockWidget
from app.ui.widgets.weather.weather_clock_controller import WeatherClockController
#from app.ui.widgets.profile.profile_view import ProfileWidget
#from app.ui.widgets.profile.profile_controller import ProfileController

class RightFrameController:
    def __init__(self, context, right_frame):
        self.context = context
        self.right_frame = right_frame
        
        self.widget_manager = WidgetManager(self.right_frame, self.context)
        
        self._init_status_bar()
        self._init_widgets()
    
    def _init_status_bar(self):
        status_bar_view = StatusBarWidget(self.right_frame)
        status_bar_controller = StatusBarController(self.right_frame, status_bar_view, self.context)
        
        self.widget_manager.register_status_bar("status_bar", status_bar_view, status_bar_controller)

    def _init_widgets(self):
        # Weather widget
        weather_widget = WeatherClockWidget(self.right_frame.widgets_frame)
        weather_controller = WeatherClockController(weather_widget)
        self.widget_manager.register("weather_widget", weather_widget, weather_controller, row=2, col=2)

        # Profile widget
        """
        profile_widget = ProfileWidget(self.right_frame.widgets_frame)
        profile_controller = ProfileController(profile_widget, self.context)
        self.widget_manager.register("profile_widget", profile_widget, profile_controller, row=0, col=0, columnspan=2)
        """

    def get_widget_controller(self, name):
        return self.widget_manager.get_widget_controller(name)