import threading
from app.ui.windows.window_conndevice import InputDeviceSelector

class StatusBarController:
    def __init__(self, root, view, context):
        self.root = root
        self.view = view
        self.context = context
        
        self.view.set_controller(self)
        self.on_sensor_count_changed = lambda count: None

    def set_on_sensor_count_changed_callback(self, on_sensor_count_changed):
        self.on_sensor_count_changed = on_sensor_count_changed

    def open_input_selector(self):
        if hasattr(self, "selector") and self.selector is not None:
            try:
                self.selector.destroy()
            except:
                pass
        self.selector = InputDeviceSelector(self.root, self.on_device_selected)

    def device_disconnect(self):
        if self.context.serial_manager:
            self.context.serial_manager.disconnect()
        
        self.context.clear_executor()

        self.view.update_status("disconn")
        self.on_sensor_count_changed(0)
        
    def on_device_selected(self, mode, port):
        if mode == "usb":
            serial = self.context.serial_manager
            serial.set_port(port)
            try:
                serial.connect()
            except Exception:
                self.view.update_status("error")
                return
            threading.Thread(target=self.threaded_handshake, daemon=True).start()
        else:
            self.view.update_status("mouse")
            if self.on_sensor_count_changed:
                self.on_sensor_count_changed(32)
            
            from app.executors.ui.ui_executor import UIExecutor
            canvas, _ = self.context.get_hexgrid()
            self.context.set_executor(UIExecutor(canvas, self.root))

    def threaded_handshake(self):
        serial = self.context.serial_manager
        data = serial.perform_handshake()
        device = data.get("device", "GRID_AI PRO") if data else None
        version = data.get("version") if data else None
        sensor_count = data.get("sensors", 32) if data else None
        
        self.root.after(0, lambda: self.update_handshake_ui(device, version, sensor_count))

    def update_handshake_ui(self, device, version, sensor_count):
        if sensor_count:
            self.context.sensor_count = sensor_count
            self.view.update_status("usb", device, version, sensor_count)
            if self.on_sensor_count_changed:
                self.on_sensor_count_changed(sensor_count)
            
            from app.executors.serial.serial_executor import SerialExecutor
            serial = self.context.serial_manager
            canvas, _ = self.context.get_hexgrid()
            self.context.set_executor(SerialExecutor(serial, canvas))

        else:
            self.view.update_status("error")
