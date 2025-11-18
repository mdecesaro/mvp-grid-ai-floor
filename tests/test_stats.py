from app.config.config import DATABASE_PATH
from app.context import AppContext
from app.stats.athlete_stats import AthleteStats

def run_tests():
    print("Running Athlete  Stats...")
    context = AppContext(None, DATABASE_PATH)
    stats = AthleteStats(context, 1, normalize_method="regression")    

if __name__ == "__main__":
    run_tests()



#python3 -m tests.test_stats

