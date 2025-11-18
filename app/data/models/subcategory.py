class Subcategory:
    def __init__(self, id=None, category_id=None, code="", name="", description=""):
        self.id = id
        self.category_id = category_id
        self.code = code
        self.name = name
        self.description = description

    def __repr__(self):
        return f"Subcategory(id={self.id}, category_id={self.category_id}, code='{self.code}', name='{self.name}', description='{self.description}')"
