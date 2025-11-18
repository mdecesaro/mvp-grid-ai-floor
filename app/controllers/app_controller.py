class AppController:
    def __init__(self, context, left_frame_controller, right_frame_controller, menu_controller):
        self.context = context
        self.left_frame_controller = left_frame_controller
        self.right_frame_controller = right_frame_controller
        self.menu_controller = menu_controller

        self._bind_events_statusbar()
    
    #### Bind events Statusbar ####
    def _bind_events_statusbar(self):
        status_bar = self.right_frame_controller.get_widget_controller("status_bar")
        status_bar.set_on_sensor_count_changed_callback(self._handle_sensor_count_update_statusbar)

    def _handle_sensor_count_update_statusbar(self, sensor_count):
        self.context.hexgrid_controller.update_layout(sensor_count)
    #### Bind events Statusbar ####