from app.data.models.category import Category
from app.data.models.subcategory import Subcategory

class CategoryDAO:
    def __init__(self, db_manager):
        self.db = db_manager

    def insert(self, category: Category):
        self.db.execute("""
            INSERT INTO categories (code, name, description)
            VALUES (?, ?, ?)
        """, (category.code, category.name, category.description))

    def get_all(self):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM categories")
        rows = cursor.fetchall()
        return [Category(**row) for row in rows]
    
    def get_by_id(self, category_id):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM categories WHERE id = ?", (category_id,))
        row = cursor.fetchone()
        return Category(**row) if row else None

    def get_by_code(self, code):
        cursor = self.db.get_cursor()
        cursor.execute("SELECT * FROM categories WHERE code = ?", (code,))
        row = cursor.fetchone()
        return Category(**row) if row else None
    

