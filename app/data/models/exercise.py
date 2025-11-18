import json

class Exercise:
    def __init__(
        self,
        category_id,
        code,
        name,
        description,
        level,
        objective,
        modality,
        parameters,
        active=1,
        board_size=14,
        category_name=None,
        id=None,
    ):
        self.id = id
        self.category_id = category_id
        self.category_name = category_name
        self.code = code
        self.name = name
        self.description = description
        self.level = level
        self.objective = objective
        self.modality = modality
        
        # parameters pode vir como JSON string → dicionário
        if isinstance(parameters, str):
            self.parameters = json.loads(parameters)
        else:
            self.parameters = parameters  # já em dicionário
        
        self.active = active
        self.board_size = board_size

    def __repr__(self):
        return (
            f"Exercise(id={self.id}, code='{self.code}', name='{self.name}', "
            f"category_id={self.category_id}, category_name='{self.category_name}', "
            f"level={self.level}, modality='{self.modality}', active={self.active}, board_size={self.board_size})"
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            category_id=row["category_id"],
            category_name=row["category_name"],
            code=row["code"],
            name=row["name"],
            description=row["description"],
            level=row["level"],
            objective=row["objective"],
            modality=row["modality"],
            parameters=row["parameters"],
            active=row["active"],
            board_size=row["board_size"]
        )

    # ===== Helper interno para acesso consistente aos parâmetros =====
    class Params:
        def __init__(self, data):
            # Desce um nível se existir 'parameters'
            if isinstance(data, dict) and 'parameters' in data:
                self.data = data['parameters']
            else:
                self.data = data

        def get(self, key, default=None):
            value = self.data.get(key, default)
            # Se for uma tupla de um elemento, retorna o elemento
            if isinstance(value, tuple) and len(value) == 1:
                return value[0]
            return value

    @property
    def p(self):
        """Retorna uma instância do helper Params para acesso seguro aos parâmetros"""
        return self.Params(self.parameters)

    @property
    def delay_min_ms(self):
        dr = self.p.get("delay_range_ms", [0])
        dtype = self.p.get("delay_type", "fixed")
        if dtype == "fixed":
            return dr[0] if dr else 0
        return min(dr) if dr else 0

    @property
    def delay_max_ms(self):
        dr = self.p.get("delay_range_ms", [0])
        dtype = self.p.get("delay_type", "fixed")
        if dtype == "fixed":
            return dr[0] if dr else 0
        return max(dr) if dr else 0

    @property
    def stimuli_count(self):
        sc = self.p.get("stimuli_count")
        if sc is not None:
            return sc
        # Se não houver, usa o tamanho do delay_range_ms se for individual
        dr = self.p.get("delay_range_ms", [])
        if self.p.get("delay_type") == "individual" and dr:
            return len(dr)
        # fallback
        return len(self.p.get("stimuli_sequence", []))
