from app.data.models.subcategory import Subcategory

class SubcategoryDAO:
    def __init__(self, db_manager):
        self.db = db_manager

    def get_subcategories_by_category_id(self, category_id):
        query = "SELECT * FROM subcategories WHERE category_id = ?"
        rows = self.db.fetchall(query, (category_id,))
        return [Subcategory(*row) for row in rows]

    def get_all_subcategories(self):
        query = "SELECT * FROM subcategories"
        rows = self.db.fetchall(query)
        return [Subcategory(*row) for row in rows]

    def delete_subcategory(self, subcategory_id):
        query = "DELETE FROM subcategories WHERE id = ?"
        self.db.execute(query, (subcategory_id,))
