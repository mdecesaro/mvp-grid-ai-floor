import threading

class SerialExecutor:
    def __init__(self, serial_manager, ui_canvas):
        self.ui_canvas = ui_canvas
        self.serial_manager = serial_manager
    
    def is_ready(self):
        return  self.ui_canvas is not None and self.serial_manager and self.serial_manager.is_connected()

    def execute(self, exercise: dict):
        def run():
            print("📤 Enviando exercício para o Arduino...")
            print(exercise.parameters)
        threading.Thread(target=run, daemon=True).start()

    def handle_result(self, data):
        print("📥 Resultado do hardware:", data)