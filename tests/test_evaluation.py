from app.data.db_manager import DatabaseManager
from app.data.dao.evaluation_dao import EvaluationDAO

from app.data.models.evaluation_test import EvaluationTest
from app.data.models.evaluation_result import EvaluationResult

def run_tests():
    print("Running Evaluation SELECT tests...")

    db = DatabaseManager("app/data/database/plataform.db")
    eval_dao = EvaluationDAO(db)

    #atl_tests = eval_dao.select_tests_by_athlete(1)
    #print(atl_tests)

    atl_tests_2 = eval_dao.select_tests_with_results_by_athlete(1)
    print(atl_tests_2)

    db.close()
    print("\n✅ Tests completed.")

if __name__ == "__main__":
    run_tests()

#python3 -m tests.test_evaluation