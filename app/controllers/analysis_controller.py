class AnalysisController:
    def __init__(self, view, context):
        self.view = view
        self.context = context
        
        self.athlete_dao = context.athlete_dao
        self.evaluation_dao = context.evaluation_dao

    def get_all_athletes(self):
        athletes = self.athlete_dao.get_all_athletes()
        return athletes

    def get_evaluation_results(self):
        return self.evaluation_dao.select_test_with_results(1, 1)
        
   