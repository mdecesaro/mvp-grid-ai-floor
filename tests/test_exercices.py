from app.data.db_manager import DatabaseManager
from app.data.dao.exercise_dao import ExerciseDAO
from app.data.models.exercise import Exercise
from app.data.models.exercise_validator import ExerciseValidator

def run_tests():
    print("Running Exercises SELECT tests...")
    

    # Test: Creating Exercice Object
    print("\n▶️ Creating Exercice:")
    exercise = Exercise(
        id=1,
        category_id=1,
        code="sv_001",
        name="Basic Light Tap",
        description="Touch the light that appears.",
        level=1,
        objective="reaction_time",
        modality="single-touch",
        parameters={
            "stimuli_count": 10,
            "delay_range_ms": [500, 1500],
            "repeat_if_wrong": True
        }
    )
    
    db = DatabaseManager("app/data/database/plataform.db") 
    exec_dao = ExerciseDAO(db)
    try:
        ExerciseValidator.validate(exercise)
        exec_dao.add_exercise(exercise)

        print("Exercise added successfully.")
    except ValueError as e:
        print(e)

    exec = exec_dao.get_exercise_by_id(1)
    print(exec)

if __name__ == "__main__":
    run_tests()


#python3 -m tests.test_exercices