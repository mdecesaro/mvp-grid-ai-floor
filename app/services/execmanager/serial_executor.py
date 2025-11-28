import threading
from _tkinter import TclError

class SerialExecutor:
    def __init__(self, serial_manager, ui_canvas):
        self.ui_canvas = ui_canvas
        self.serial_manager = serial_manager

        self.plan = None
        self.on_log = None
        self.on_finish_test = None

        self.active = False     

    def set_plan(self, plan):
        self.plan = plan
    
    def set_callbacks(self, on_log=None, on_finish_test=None):
        self.on_log = on_log
        self.on_finish_test = on_finish_test

    def _log(self, msg):
        if callable(self.on_log):
            self.on_log(msg)

    def is_ready(self):
        return  self.ui_canvas is not None and self.serial_manager and self.serial_manager.is_connected()

    def execute(self):
        if not self.plan:
            raise RuntimeError("Nenhum plano definido.")
        if self.active:
            self._log("⚠️ Execução já em andamento.")
            return
        

        print(self.plan.get_execution_plan())
        '''
        self.active = True
        self.serial_manager.send_command("SET|14|0|700|1|008000")
        self._log("➡️ Enviado: SET")
        if not self._wait_for_set_ok(timeout=2.0):
            self._log("❌ Falha: Arduino não confirmou SET.")
            self.active = False
            return
        self._log("✔️ SET confirmado. Enviando START...")
        self.serial_manager.send_command("START")
        t = threading.Thread(target=self._listen_thread, daemon=True)
        t.start()
        '''
    def _wait_for_set_ok(self, timeout=2.0):
        import time
        start = time.time()

        while time.time() - start < timeout:
            line = self.serial_manager.read_line()
            if not line:
                continue

            line = line.strip()

            if line == "SET_OK":
                return True
            
            if line == "SET_ERROR":
                return False

        return False

    def _listen_exercise_events(self):
        while self.active:
            line = self.serial_manager.read_line()
            if not line:
                continue

            line = line.strip()
            self._log(f"📨 Evento: {line}")

            if line.startswith("EVT"):
                self._handle_event(line)

            if line == "DONE":
                break

        try:
            self._log("🏁 Execução finalizada.")
        except TclError:
            pass

    def _listen_thread(self):
        try:
            self._listen_exercise_events()
        finally:
            self.finish()

    def _handle_event(self, evt_line):
        try:
            parts = evt_line.split("|")
            evt = parts[1]

            if evt == "ON":
                sensor = 1#int(parts[2])
                self.ui_canvas.turn_on(sensor, "#5CE65C")
            elif evt == "HIT":
                sensor = int(parts[2])
                ms = int(parts[3])
            elif evt == "OFF":
                sensor = int(parts[2])
                self.ui_canvas.turn_off(1)    
        except TclError:
            pass
    
    # ===== Finalização =====
    def finish(self):
        if not self.active:
            return
        self.active = False
        self._log("🏁 DONE - Execução finalizada.")
        
        if callable(self.on_finish_test):
            self.on_finish_test("DONE")

    def handle_result(self, data):
        print("📥 Resultado do hardware:", data)

   