
class MenuController:
    def __init__(self, view, context):
        self.view = view
        self.context = context

        self._setup_menu()

    def _setup_menu(self):
        self.view.add_athlete_command("➕ New Athlete", self.open_new_athlete_window)

        self.view.add_exercise_command("🧱 Exercice Library", self.open_exercices_window)
        self.view.add_exercise_command("🧪 Performance Testing", self.open_performance_window)
        self.view.add_exercise_command("📊 Performance Analysis", self.open_evaluation_window)

    def open_new_athlete_window(self):
        self.context.window_manager.open_new_athlete("new_athlete")

    def open_exercices_window(self):
        self.context.window_manager.open_exercice_library("exercice_library")

    def open_performance_window(self):
        self.context.window_manager.open_performance_testing("performance_testing")
    
    def open_evaluation_window(self):
        self.context.window_manager.open_evaluation_testing("evaluation_testing")