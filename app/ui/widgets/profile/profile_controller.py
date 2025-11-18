from app.ui.windows.listathlete_view import ListAthleteView
from app.controllers.list_athlete_controller import ListAthleteController

class ProfileController:
    def __init__(self, view, context):
        self.view = view
        self.context = context
        self.athlete_view = None
        self.view.set_controller(self)
        self.context.subscribe_to_athlete_change(self._update_profile)
    
    def _update_profile(self, athlete):
        if athlete is None:
            self.view.clear_fields()
        else:
            self.athlete = athlete
            self.athlete_view.destroy()
            self.athlete_view = None
            self.view.display_profile(athlete)
            
    def load_athlete(self):
        if self.athlete_view is None or not self.athlete_view.winfo_exists():
            self.list_controller = ListAthleteController(None, self.context)  
            self.athlete_view = ListAthleteView(self.view, self.list_controller)
            self.list_controller.set_view(self.athlete_view)  
        else:
            self.athlete_view.lift()

    def clear_athlete(self):
        self.context.clear_athlete()

    