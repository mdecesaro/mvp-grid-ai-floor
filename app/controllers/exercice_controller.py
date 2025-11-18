class ExerciceController:
    def __init__(self, view, context):
        self.view = view
        self.context = context
        self.exercise_dao = context.exercise_dao

    def load_exercises(self):
        exercises = self.exercise_dao.get_all_exercises()
        self.view.clear_table()
        self.view.insert_into_table(exercises)
    
    def load_exercise_into_form(self, exercise_code):
        exercise = self.exercise_dao.get_exercise_by_code(exercise_code)
        if exercise:
            self.view.fill_form(exercise)

    def get_categories(self):
        categories = self.context.category_dao.get_all()
        return [(cat.id, cat.name) for cat in categories]
        
    def add_exercise(self, exercise):
        self.exercise_dao.add_exercise(exercise)
        
    def update_exercise(self, exercise):
        self.exercise_dao.update_exercise(exercise)
        