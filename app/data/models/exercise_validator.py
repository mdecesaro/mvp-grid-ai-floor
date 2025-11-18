from app.data.models.exercise import Exercise

class ExerciseValidator:
    VALID_MODALITIES = {"single-touch", "multi-touch", "sequence", "timed", "challenge"}

    @staticmethod
    def validate(exercise: Exercise):
        errors = []

        if exercise.modality not in ExerciseValidator.VALID_MODALITIES:
            errors.append(f"Modality '{exercise.modality}' is invalid.")
        if not isinstance(exercise.parameters, dict):
            errors.append("Parameters must be a dictionary.")
        if not (1 <= exercise.level <= 10):
            errors.append("Level must be between 1 and 10.")

        if errors:
            raise ValueError("Validation errors: " + "; ".join(errors))
