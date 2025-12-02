import time
import random
from app.data.models.evaluation_result import EvaluationResult

class UIExecutor:
    def __init__(self, ui_canvas, root):
        self.root = root
        self.ui_canvas = ui_canvas
        
        self.ui_canvas.on_sensor_click = self.register_click
        
        self.plan = None
        self.on_log = None
        self.on_finish_test = None
        
        self.steps = []
        self.current_step = 0
        self.results = []
        self.active = False
        
        self.target_sensor = None
        self.start_time = None
        self.repeat_if_wrong = False
        self.awaiting_click = False
        self.total_execution_time = None

    def is_ready(self):
        return self.ui_canvas is not None
    
    def set_plan(self, plan):
        self.plan = plan
    
    def set_callbacks(self, on_log=None, on_finish_test=None):
        self.on_log = on_log
        self.on_finish_test = on_finish_test

    def _log(self, msg):
        if callable(self.on_log):
            self.on_log(msg)

    # ===== Execução =====
    def execute(self):
        if not self.plan:
            raise RuntimeError("Nenhum plano definido.")
        if self.active:
            self._log("⚠️ Execução já em andamento.")
            return

        self.steps = self.plan.get_execution_plan()
        self.current_step = 0
        self.results.clear()
        self.active = True
        self.total_execution_time = time.time()

        # Primeiro step: pega o delay inicial
        first_step = self.steps[0]
        self.delay_ms = first_step.get('delay_ms', 0)
        self.root.after(self.delay_ms, self.next_step)

    def next_step(self):
        if not self.active or self.current_step >= len(self.steps):
            self.finish()
            return
        
        step = self.steps[self.current_step]
        if self.current_step > 0:
            self.delay_ms = step.get('delay_ms', 0)

        self.target_sensor = step['stimulus_id']
        self.repeat_if_wrong = step.get('repeat_if_wrong', False)
        self.stimulus_type = step['stimulus_type']
        self.distractor_type = step['distractor_type']
        self.active_distractors = []

        # Acende o estímulo
        self.correct_color = step.get('correct_color') if step.get('stimulus_type') == 'color' else None
        self.ui_canvas.turn_on(self.target_sensor, self.correct_color or "#5CE65C")

        # Luzes de distração
        if 'distractor_colors' in step and step['distractor_colors']:
            len_sensors = self.ui_canvas.len_sensors()
            available_sensors = [sid for sid in range(1, len_sensors + 1) if sid != self.target_sensor]
            chosen_sensors = random.sample(available_sensors, min(len(step['distractor_colors']), len(available_sensors)))
            for sensor_id, color in zip(chosen_sensors, step['distractor_colors']):
                self.ui_canvas.turn_on(sensor_id, color)
                self.active_distractors.append({"id": sensor_id, "color": color})

        self.start_time = time.time()
        self.awaiting_click = True

    # ===== Clique ou timeout =====
    def register_click(self, sensor_id):
        if not self.active or not self.awaiting_click:
            return
        self._handle_response(sensor_id, click_type="click")

    def handle_timeout(self):
        if not self.active or not self.awaiting_click:
            return
        self._handle_response("timeout", click_type="timeout")

    def _handle_response(self, sensor_id, click_type="click"):
        step = self.steps[self.current_step]
        expected_id = self.target_sensor
        click_timestamp = time.time()
        reaction_time_ms = None if click_type == "timeout" else (click_timestamp - self.start_time) * 1000
        elapsed_since_start = (click_timestamp - self.total_execution_time) * 1000

        is_error = (sensor_id != expected_id)
        wrong_id = sensor_id if is_error else 0

        self.record_result(
            step['round'],
            expected_id,
            reaction_time_ms,
            is_error,
            wrong_id,
            click_timestamp if click_type != "timeout" else None,
            elapsed_since_start
        )

        # Desliga estímulo e distractors
        self.ui_canvas.turn_off(expected_id)
        for d in self.active_distractors:
            self.ui_canvas.turn_off(d["id"])
        self.active_distractors.clear()

        # Log
        if click_type == "click":
            msg = f"❌ Errou! Clicou {sensor_id}" if is_error else f"✅ Acertou {sensor_id} em {reaction_time_ms:.1f}ms"
        else:
            msg = f"⏱ Timeout no sensor {expected_id}"
        self._log(msg)

        # Avança para o próximo passo
        if not is_error or not self.repeat_if_wrong:
            self.current_step += 1

        self.awaiting_click = False
        if self.current_step < len(self.steps):
            self.root.after(self.delay_ms, self.next_step)
        else:
            self.finish()

    # ===== Registro de resultados =====
    def record_result(self, round_num, stim_id, reaction_time_ms, error, wrong_id, click_timestamp, elapsed_since_start):
        sensor = self.ui_canvas.get_sensor_by_id(stim_id)
        stimulus_position = sensor.sector if sensor else "unknown"
        foot_used = sensor.expected_foot if sensor else "unknown"

        eval_result = EvaluationResult(
            round_num=round_num,
            stimulus_id=stim_id,
            stimulus_position=stimulus_position,
            stimulus_type=self.stimulus_type,
            correct_color=self.correct_color,
            reaction_time=reaction_time_ms,
            stimulus_start=self.start_time,
            stimulus_end=click_timestamp,
            delay_ms=self.delay_ms,
            elapsed_since_start=elapsed_since_start,
            error=int(error),
            foot_used=foot_used,
            wrong_stimulus_id=wrong_id,
            distractor_type=getattr(self, "distractor_type", None),
            distractor_id_color=[{"id": d["id"], "color": d["color"]} for d in getattr(self, "active_distractors", [])]
        )
        self.results.append(eval_result)

    # ===== Finalização =====
    def finish(self):
        if not self.active:
            return
        self.active = False
        self._log("🏁 Execução finalizada.")
        
        if callable(self.on_finish_test):
            self.on_finish_test(self.results)
        
    def get_results(self):
        return self.results
