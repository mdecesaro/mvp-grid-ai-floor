import json
import random
from typing import List, Dict, Any
from jsonschema import validate, ValidationError

exercise_schema = exercise_schema = {
    "type": "object",
    "properties": {
        "category": {"type": "string", "enum": ["Performance"]},
        "modality": {"type": "string", "enum": ["Single-Touch"]},
        "parameters": {
            "type": "object",
            "properties": {
                "stimuli_count": {"type": "integer", "minimum": 1},
                "stimuli_generation_mode": {"type": "string", "enum": ["defined", "random", "ai_generated", "adaptive", "pattern_based"]},
                "stimuli_sequence": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 1}
                },
                "stimulus_type": {
                    "type": "string",
                    "enum": ["color", "position", "multi_light", "fake_light", "timed", "pattern"],
                    "description": "Type of stimulus presented in the exercise step."
                },
                "correct_color": {
                    "anyOf": [
                        { "type": "string", "pattern": "^#([A-Fa-f0-9]{6})$" },
                        { "type": "string", "enum": ["green", "red", "yellow", "blue"] }
                    ],
                    "description": "The color that represents the correct target for the athlete. Can be a named color or a hexadecimal code."
                },
                "distractor_type": {
                    "type": "string",
                    "enum": ["color", "position", "multi_light", "fake_light", "timed", "pattern"],
                    "description": "Type of distractor stimulus presented in the exercise step."
                },
                "distractor_colors": {
                    "anyOf": [
                        { 
                            "type": "array", 
                            "items": { 
                                "anyOf": [
                                { "type": "string", "pattern": "^#([A-Fa-f0-9]{6})$" },
                                { "type": "string", "enum": ["green", "red", "yellow", "blue"] }
                                ]
                            } 
                        }
                    ],
                    "description": "Colors used as false stimuli or 'random' to pick distractor colors automatically. Can be named colors or hexadecimal codes."
                },
                "distractor_ncolors_at_time": {
                    "type": "integer",
                    "minimum": 0,
                    "description": "Number of distractor simultaneous colors to light up along with the correct color."
                },
                "delay_type": {"type": "string", "enum": ["fixed", "range", "individual"]},
                "delay_range_ms": {
                    "type": "array",
                    "items": {"type": "integer", "minimum": 0}
                },
                "execution_rounds": {"type": "integer", "minimum": 1},
                "timeout_ms": {
                    "anyOf": [
                        {"type": "integer", "minimum": 0},
                        {"type": "null"}
                    ]
                },
                "repeat_if_wrong": {"type": "boolean"}
            },
            "required": [
                "stimuli_count",
                "stimuli_generation_mode",
                "stimuli_sequence",
                "stimulus_type",
                "correct_color",
                "delay_type",
                "delay_range_ms",
                "execution_rounds"
            ],
            "additionalProperties": False
        }
    },
    "required": ["category", "modality", "parameters"],
    "additionalProperties": False
}



## pensar em implementar exames de salto na plataforma da Vald e usar para ML
class UIExercisePlan:
    def __init__(self, exercise, athlete):
        self.exercise = exercise
        self.athlete = athlete

        # 1. Extrair os parâmetros (mesma lógica de antes)
        params = exercise.parameters
        if isinstance(params, str):
            import json
            params = json.loads(params)
        if 'parameters' in params:
            params = params['parameters']

        # 2. Montar o mesmo dicionário antigo para validar e usar
        self.raw_data = {
            "category": exercise.category_name,
            "modality": exercise.modality,
            "parameters": params
        }

        self.parameters = self.raw_data["parameters"]
        self.validate_schema()
        self.validate_logic() 
        self.build_stimuli_sequence()
        self.build_delays()
        self.validate_final_plan()

    def _parse_parameters(self, params):
        if isinstance(params, str):
            import json
            params = json.loads(params)
        if "parameters" in params:
            params = params["parameters"]
        return params

    def validate_schema(self):
        try:
            validate(instance=self.raw_data, schema=exercise_schema)
        except ValidationError as e:
            raise ValueError(f"Erro na validação do JSON: {e.message}")

    def validate_logic(self):
        self.st_type = self.parameters["stimulus_type"]

        if self.st_type == "color":
            if "correct_color" not in self.parameters:
                raise ValueError("'correct_color' must be defined for color stimulus")

            distractor_type = self.parameters.get("distractor_type")
            if distractor_type:
                distractors = self.parameters.get("distractor_colors", [])
                distractors_num = self.parameters.get("distractor_num", 0)

                if not isinstance(distractors, list):
                    raise ValueError("'distractor_colors' must be a list if distractor_type is defined")
                if not isinstance(distractors_num, int):
                    raise ValueError("'distractor_num' must be an integer")
                if distractors_num > len(distractors):
                    raise ValueError("'distractor_num' cannot exceed number of defined distractor colors")

        elif self.st_type in ["multi_light", "fake_light", "pattern", "position", "timed"]:
            # regras específicas de cada tipo podem ser definidas aqui
            pass
        else:
            raise ValueError(f"Unsupported stimulus_type: {self.st_type}")

    
    def build_stimuli_sequence(self):
        stimuli_count = self.parameters["stimuli_count"]
        stimuli_generation_mode = self.parameters["stimuli_generation_mode"]

        if stimuli_generation_mode == "random":
            sequence = list(range(1, stimuli_count + 1))
            random.shuffle(sequence)
            self.parameters["stimuli_sequence"] = sequence

        elif stimuli_generation_mode == "defined":
            sequence = self.parameters["stimuli_sequence"]
            if len(sequence) != stimuli_count:
                raise ValueError(
                    f"stimuli_sequence deve ter {stimuli_count} elementos, mas tem {len(sequence)}"
                )

    def build_delays(self):
        delay_type = self.parameters["delay_type"]
        delay_range_ms = self.parameters["delay_range_ms"]
        stimuli_count = self.parameters["stimuli_count"]

        if delay_type == "fixed":
            if len(delay_range_ms) != 1:
                raise ValueError("delay_range_ms deve ter 1 valor para delay_type='fixed'")
            self.parameters["final_delays"] = [delay_range_ms[0]] * stimuli_count

        elif delay_type == "range":
            if len(delay_range_ms) != 2:
                raise ValueError("delay_range_ms deve ter 2 valores [min, max] para delay_type='range'")
            min_d, max_d = delay_range_ms
            self.parameters["final_delays"] = [
                random.randint(min_d, max_d) for _ in range(stimuli_count)
            ]

        elif delay_type == "individual":
            if len(delay_range_ms) != stimuli_count:
                raise ValueError(f"delay_range_ms deve ter {stimuli_count} valores para delay_type='individual'")
            self.parameters["final_delays"] = delay_range_ms.copy()

    def validate_final_plan(self):
        if len(self.parameters["stimuli_sequence"]) != self.parameters["stimuli_count"]:
            raise ValueError("stimuli_sequence final não bate com stimuli_count")
        if len(self.parameters["final_delays"]) != self.parameters["stimuli_count"]:
            raise ValueError("final_delays não bate com stimuli_count")

    def get_execution_plan(self) -> List[Dict[str, Any]]:
        plan = []
        
        for round_num in range(self.parameters["execution_rounds"]):
            for i, stimulus in enumerate(self.parameters["stimuli_sequence"]):
                entry = {
                    "round": round_num + 1,
                    "stimulus_id": stimulus,
                    "delay_ms": self.parameters["final_delays"][i],
                    "stimulus_type": self.st_type
                }

                # Campos opcionais
                timeout = self.parameters.get("timeout_ms")
                if timeout is not None:
                    entry["timeout_ms"] = timeout

                entry["repeat_if_wrong"] = self.parameters.get("repeat_if_wrong", False)

                # Campos para estímulo do tipo "color"
                if self.st_type == "color":
                    entry["correct_color"] = self.parameters.get("correct_color")

                    distractor_type = self.parameters.get("distractor_type")
                    distractors = self.parameters.get("distractor_colors")
                    distractors_num = self.parameters.get("distractor_ncolors_at_time", 0)
                    entry["distractor_type"] = distractor_type
                    if distractor_type == "color" and distractors and distractors_num > 0:
                        if isinstance(distractors, list):
                            entry["distractor_colors"] = random.sample(
                                distractors, min(distractors_num, len(distractors))
                            )
                        elif distractors == "random":
                            # gerar cores aleatórias, ex.: escolher do enum ou hexadecimal
                            entry["distractor_colors"] = random.sample(
                                ["red", "yellow", "blue"], distractors_num
                            )

                plan.append(entry)

        return plan




