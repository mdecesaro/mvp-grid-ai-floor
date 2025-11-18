from app.data.models.exercise import Exercise
import json

class ExerciseDAO:
    def __init__(self, db_manager):
        self.db = db_manager
        
    def add_exercise(self, exercise: Exercise):
        cursor = self.db.get_cursor()
        cursor.execute(
            "SELECT id FROM categories WHERE id = ?",
            (exercise.category_id,)
        )
        row = cursor.fetchone()
        if row is None:
            raise ValueError("Category code not found.")
        cat_id = row["id"]
        
        cursor.execute("""
            INSERT INTO exercises (
                category_id, code, name, description,
                level, objective, modality,
                parameters, board_size
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cat_id, exercise.code, exercise.name, exercise.description,
            exercise.level, exercise.objective, exercise.modality, 
            json.dumps(exercise.parameters), int(exercise.board_size)
        ))
        self.db.commit()
    
    def update_exercise(self, exercise):
        cursor = self.db.get_cursor()
        cursor.execute("""
            UPDATE exercises
            SET category_id = ?, code = ?, name = ?, description = ?, level = ?, 
                objective = ?, modality = ?, parameters = ?, board_size = ?
            WHERE id = ?
        """, (
            exercise.category_id,
            exercise.code,
            exercise.name,
            exercise.description,
            exercise.level,
            exercise.objective,
            exercise.modality,
            json.dumps(exercise.parameters),
            exercise.board_size,
            exercise.id
        ))
        self.db.commit()


    def get_exercise_by_code(self, exercise_code: int) -> Exercise:
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT 
                e.id,
                e.category_id,
                c.name AS category_name,
                e.code,
                e.name,
                e.description,
                e.level,
                e.objective,
                e.modality,
                e.parameters,
                e.active,
                e.board_size
            FROM exercises e
            JOIN categories c ON e.category_id = c.id WHERE e.code = ?
        """, (exercise_code,))
        row = cursor.fetchone()
        if row:
            return Exercise.from_row(row)
        else:
            raise ValueError(f"Exercise with id {exercise_code} not found.")
        
    def get_exercise_by_id(self, exercise_id: int) -> Exercise:
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT * FROM exercises WHERE id = ?
        """, (exercise_id,))
        row = cursor.fetchone()
        if row:
            return Exercise.from_row(row)
        else:
            raise ValueError(f"Exercise with id {exercise_id} not found.")

    def get_all_exercises(self):
        cursor = self.db.get_cursor()
        cursor.execute("""
            SELECT 
                e.id,
                e.category_id,
                c.name AS category_name,
                e.code,
                e.name,
                e.description,
                e.level,
                e.objective,
                e.modality,
                e.parameters,
                e.active,
                e.board_size
            FROM exercises e
            JOIN categories c ON e.category_id = c.id
            ORDER BY e.id
        """)
        rows = cursor.fetchall()
        return [Exercise.from_row(row) for row in rows]


    