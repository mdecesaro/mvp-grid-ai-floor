class ListAthleteController:
    def __init__(self, view, context):
        self.view = view
        self.context = context
        self.athlete_dao = context.athlete_dao

    def set_view(self, view):
        self.view = view

    def get_athletes(self):
        return self.athlete_dao.get_all_athletes()
    
    def athlete_selected(self, athlete_id):
        athlete = self.athlete_dao.get_athlete_by_id(athlete_id)
        self.context.set_athlete(athlete)
       