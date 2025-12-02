from app.executors.serial.serial_builder import SerialBuilder
from app.executors.ui.ui_builder import UIBuilder
from app.data.models.evaluation_test import EvaluationTest
import time

class PerformanceController:
    def __init__(self, view, context):
        self.view = view
        self.context = context
        self.exercise_dao = context.exercise_dao
        self.athlete_dao = context.athlete_dao
        self.executor_manager = context.executor_manager
        self.evaluation_dao = context.evaluation_dao

    def load_data(self):
        try:
            exercises = self.exercise_dao.get_all_exercises_by_size(self.context.device_layout.sensor_count)
            self.view.populate_exercises(exercises)

            athletes = self.athlete_dao.get_all_athletes()
            self.view.populate_athletes(athletes)

            self.view._log("✅ Dados carregados com sucesso.")
        except Exception as e:
            self.view._log(f"❌ Erro ao carregar dados: {e}")

    def start_evaluation(self, athlete, exercise):
        if not self.executor_manager:
            self.view._log("❌ Nenhum gerenciador de exercício definido.")
            return
        if not self.executor_manager.is_ready():
            self.view._log("⚠️ Executor não está pronto. Verifique a conexão ou modo de execução.")
            return
        
        try:
            # Salvar as infos mínimas necessárias para criar Test
            self.current_athlete_id = athlete.id
            self.current_exercise_id = exercise.id
            self.current_device_id = "device_xyz"  # ou pegar do executor
            self.current_platform_version = "1.0.0"

            # Usando o helper Params
            self.current_delay_type = exercise.p.get("delay_type", "fixed")
            self.current_execution_rounds = exercise.p.get("execution_rounds", 1)

            self.stimuli_count=exercise.stimuli_count
            self.delay_min_ms=exercise.delay_min_ms
            self.delay_max_ms=exercise.delay_max_ms

            self.current_timeout_ms = exercise.p.get("timeout_ms", 0)
            self.current_repeat_if_wrong = exercise.p.get("repeat_if_wrong", False)
            
            if(self.context.device_layout.sensor_count == 32):
                ui_plan = UIBuilder(exercise, athlete)
            else:
                ui_plan = SerialBuilder(exercise, athlete)

            self.executor_manager.executor.set_callbacks(
                on_log=lambda msg: self._on_log(msg),
                on_finish_test=lambda test_id: self._on_finish_test(test_id)
            )
            self.executor_manager.load_plan(ui_plan)
            self.executor_manager.start()
            
            self.view._log("🏁 Teste iniciado com sucesso.")
        except Exception as e:
            self.view._log(f"❌ Erro ao iniciar teste: {e}")

    def _on_finish_test(self, test_results):
        if(test_results == "DONE"):
            return
        
        total_attempts = len(test_results)
        hits = sum(1 for r in test_results if not r.error)
        errors = sum(1 for r in test_results if r.error)
        reaction_times = [r.reaction_time for r in test_results if r.reaction_time is not None]
        avg_reaction_time = sum(reaction_times) / max(1, len(reaction_times))
        duration_ms = sum(reaction_times)

        eval_test = EvaluationTest(
            athlete_id=self.current_athlete_id,
            exercise_id=self.current_exercise_id,
            device_id=self.current_device_id,
            platform_version=self.current_platform_version,
            timestamp=time.time(),
            stimuli_count=self.stimuli_count,
            delay_type=self.current_delay_type,
            delay_min_ms=self.delay_min_ms,
            delay_max_ms=self.delay_max_ms,
            execution_rounds=self.current_execution_rounds,
            timeout_ms=self.current_timeout_ms,
            repeat_if_wrong=self.current_repeat_if_wrong,
            total_attempts=total_attempts,
            hits=hits,
            errors=errors,
            avg_reaction_time=avg_reaction_time,
            duration_ms=duration_ms,
            results=test_results
        )
        # Salvar no banco de dados
        test_id = self.evaluation_dao.insert_test_result(eval_test)
        self._on_log(f"✅ Teste salvo no banco com id {test_id}")

    def cleanup(self):
        """Limpa recursos e remove callbacks para evitar chamadas indevidas."""
        if self.executor_manager and self.executor_manager.executor:
            self.executor_manager.executor.set_callbacks(
                on_log=None,
                on_finish_test=None
            )
        self.view = None
        self.context = None  
        
    def _on_log(self, msg):
        self.view._log(msg)