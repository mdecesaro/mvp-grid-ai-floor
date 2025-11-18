from datetime import datetime

class Athlete:
    def __init__(self, id=None, name="", gender="", country="", birth="", dominant_foot="", position="", profile=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.country = country
        self.birth = birth
        self.dominant_foot = dominant_foot
        self.position = position
        self.profile = profile
    
    def __repr__(self):
        return f"Athlete(id={self.id}, name='{self.name}', gender='{self.gender}', country='{self.country}', birth='{self.birth}'), dominant_foot='{self.dominant_foot}'), position='{self.position}') " 
    
    def get_age(self):
        try:
            nascimento = datetime.strptime(self.birth, "%d/%m/%Y")
            hoje = datetime.today()
            idade = hoje.year - nascimento.year
            if (hoje.month, hoje.day) < (nascimento.month, nascimento.day):
                idade -= 1
            return idade
        except ValueError:
            return None
    
    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            name=row["name"],
            gender=row["gender"],
            country=row["country"],
            birth=row["birth"],
            dominant_foot=row["dominant_foot"],
            position=row["position"],
            profile=row["profile"]
        )