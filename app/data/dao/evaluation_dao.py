from app.data.models.evaluation_test import EvaluationTest
from app.data.models.evaluation_result import EvaluationResult
import json

class EvaluationDAO:
    def __init__(self, db_manager):
        self.db = db_manager

    def insert_test_result(self, eval_test: EvaluationTest):
        try:
            with self.db:
                cursor = self.db.get_cursor()
                
                # ===== Inserir avaliação =====
                cursor.execute("""
                    INSERT INTO evaluation_tests (
                        athlete_id,
                        exercise_id,
                        device_id,
                        platform_version,
                        timestamp,
                        stimuli_count,
                        delay_type,
                        delay_min_ms,
                        delay_max_ms,
                        execution_rounds,
                        timeout_ms,
                        repeat_if_wrong,
                        total_attempts,
                        hits,
                        errors,
                        avg_reaction_time,
                        duration_ms
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    eval_test.athlete_id,
                    eval_test.exercise_id,
                    eval_test.device_id,
                    eval_test.platform_version,
                    eval_test.timestamp,
                    eval_test.stimuli_count,
                    eval_test.delay_type,
                    eval_test.delay_min_ms,
                    eval_test.delay_max_ms,
                    eval_test.execution_rounds,
                    eval_test.timeout_ms,
                    int(eval_test.repeat_if_wrong),
                    eval_test.total_attempts,
                    eval_test.hits,
                    eval_test.errors,
                    eval_test.avg_reaction_time,
                    eval_test.duration_ms
                ))
                
                test_id = cursor.lastrowid
                
                # ===== Inserir todos os resultados de uma vez =====
                results_data = [
                    (
                        test_id,
                        r.round_num,
                        r.stimulus_id,
                        r.stimulus_position,
                        r.stimulus_type,
                        r.reaction_time,
                        r.stimulus_start,
                        r.stimulus_end,
                        r.delay_ms,
                        r.elapsed_since_start,
                        int(r.error),
                        r.foot_used,
                        r.wrong_stimulus_id,
                        r.correct_color,
                        r.distractor_type,
                        json.dumps(r.distractor_id_color)
                    )
                    for r in eval_test.results
                ]
                
                cursor.executemany("""
                    INSERT INTO evaluation_test_results (
                        test_id,
                        round_num,
                        stimulus_id,
                        stimulus_position,
                        stimulus_type,
                        reaction_time,
                        stimulus_start,
                        stimulus_end,
                        delay_ms,
                        elapsed_since_start,
                        error,
                        foot_used,
                        wrong_stimulus_id,
                        correct_color,
                        distractor_type,
                        distractor_id_color
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, results_data)
                
                return test_id

        except Exception as e:
            raise RuntimeError(f"Falha ao salvar Test + Results: {e}")

    # ===================== SELECT =====================
    def select_tests_by_athlete(self, athlete_id: int):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT *
            FROM evaluation_tests
            WHERE athlete_id = ?
            ORDER BY timestamp DESC
        """, (athlete_id,))
        rows = cursor.fetchall()
        tests = []
        for row in rows:
            tests.append(EvaluationTest(
                id=row["id"],
                athlete_id=row["athlete_id"],
                exercise_id=row["exercise_id"],
                device_id=row["device_id"],
                platform_version=row["platform_version"],
                timestamp=row["timestamp"],
                stimuli_count=row["stimuli_count"],
                delay_type=row["delay_type"],
                delay_min_ms=row["delay_min_ms"],
                delay_max_ms=row["delay_max_ms"],
                execution_rounds=row["execution_rounds"],
                timeout_ms=row["timeout_ms"],
                repeat_if_wrong=bool(row["repeat_if_wrong"]),
                total_attempts=row["total_attempts"],
                hits=row["hits"],
                errors=row["errors"],
                avg_reaction_time=row["avg_reaction_time"],
                duration_ms=row["duration_ms"],
                results=[]  # não carregamos os resultados aqui
            ))
        return tests

    def select_test_with_results(self, test_id: int, athlete_id: int = None):
        cursor = self.db.get_cursor()
        if athlete_id is not None:
            cursor.execute("""
                SELECT *
                FROM evaluation_tests
                WHERE id = ? AND athlete_id = ?
            """, (test_id, athlete_id))
        else:
            cursor.execute("""
                SELECT *
                FROM evaluation_tests
                WHERE id = ?
            """, (test_id,))

        row = cursor.fetchone()
        if not row:
            return None

        # Recupera resultados
        cursor.execute("""
            SELECT *
            FROM evaluation_test_results
            WHERE test_id = ?
            ORDER BY round_num ASC
        """, (test_id,))
        result_rows = cursor.fetchall()
        results = []
        for r in result_rows:
            distractors = json.loads(r["distractor_id_color"]) if r["distractor_id_color"] not in (None, "", "null") else []
            results.append(EvaluationResult(
                id=r["id"],
                test_id=r["test_id"],
                round_num=r["round_num"],
                stimulus_id=r["stimulus_id"],
                stimulus_position=r["stimulus_position"],
                stimulus_type=r["stimulus_type"],
                correct_color=r["correct_color"],
                reaction_time=r["reaction_time"],
                stimulus_start=r["stimulus_start"],
                stimulus_end=r["stimulus_end"],
                delay_ms=r["delay_ms"],
                elapsed_since_start=r["elapsed_since_start"],
                error=bool(r["error"]),
                foot_used=r["foot_used"],
                wrong_stimulus_id=r["wrong_stimulus_id"],
                distractor_type=r["distractor_type"],
                distractor_id_color=distractors
            ))
        
        eval_test = EvaluationTest(
            id=row["id"],
            athlete_id=row["athlete_id"],
            exercise_id=row["exercise_id"],
            device_id=row["device_id"],
            platform_version=row["platform_version"],
            timestamp=row["timestamp"],
            stimuli_count=row["stimuli_count"],
            delay_type=row["delay_type"],
            delay_min_ms=row["delay_min_ms"],
            delay_max_ms=row["delay_max_ms"],
            execution_rounds=row["execution_rounds"],
            timeout_ms=row["timeout_ms"],
            repeat_if_wrong=bool(row["repeat_if_wrong"]),
            total_attempts=row["total_attempts"],
            hits=row["hits"],
            errors=row["errors"],
            avg_reaction_time=row["avg_reaction_time"],
            duration_ms=row["duration_ms"],
            results=results
        )
        return eval_test

    def select_data_for_training(self):
        cursor = self.db.get_cursor()
        cursor.execute("""
                    SELECT 
                        t.id AS test_id,
                        t.athlete_id,
                        t.exercise_id,
                        t.device_id,
                        t.platform_version,
                        t.timestamp,
                        t.stimuli_count,
                        t.delay_type,
                        t.delay_min_ms,
                        t.delay_max_ms,
                        t.execution_rounds,
                        t.timeout_ms,
                        t.repeat_if_wrong,
                        t.total_attempts,
                        t.hits,
                        t.errors,
                        t.avg_reaction_time,
                        t.duration_ms,

                        r.id AS result_id,
                        r.test_id AS result_test_id,
                        r.round_num,
                        r.stimulus_id,
                        r.stimulus_position,
                       
                        s.dist_center_cm,
                        s.q,
                        s.r,
                        s.x_c,
                        s.y_c,
                        s.angle_norm,
                        s.sector,
                       
                        r.stimulus_type,
                        r.correct_color,
                        ROUND(r.reaction_time, 1) AS reaction_time,
                        r.stimulus_start,
                        r.stimulus_end,
                        r.delay_ms,
                        r.elapsed_since_start,
                        r.error,
                        r.foot_used,
                        r.wrong_stimulus_id,
                        r.distractor_type,
                        r.distractor_id_color
                    FROM evaluation_tests t
                    LEFT JOIN evaluation_test_results r ON t.id = r.test_id
                    LEFT JOIN sensors s ON r.stimulus_id = s.sensor
                    WHERE s.layout = "pro"
                    ORDER BY t.id, r.round_num ASC;
                """)
        
        rows = cursor.fetchall()
        
        return [dict(row) for row in rows]