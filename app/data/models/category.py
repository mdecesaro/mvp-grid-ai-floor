class Category:
    def __init__(self, id=None, code="", name="", description="", subcategories=None):
        self.id = id
        self.code = code.strip()
        self.name = name.strip()
        self.description = description.strip()
        
    def __repr__(self):
        return (f"Category(id={self.id}, code='{self.code}', name='{self.name}', "
                f"description='{self.description}')")

    def to_dict(self):
        return {
            "id": self.id,
            "code": self.code,
            "name": self.name,
            "description": self.description
        }
