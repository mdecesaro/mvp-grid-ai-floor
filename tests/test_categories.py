from app.data.db_manager import DatabaseManager
from app.data.dao.category_dao import CategoryDAO


def run_tests():
    print("Running category and subcategory SELECT tests...")

    db = DatabaseManager("app/data/database/plataform.db")  # Substitua com o caminho real do seu banco
    category_dao = CategoryDAO(db)

    # Test: Get all categories
    print("\n▶️ All categories:")
    categories = category_dao.get_all()
    for cat in categories:
        print(cat)
    
    db.close()
    print("\n✅ Tests completed.")

if __name__ == "__main__":
    run_tests()


#python3 -m tests.test_categories