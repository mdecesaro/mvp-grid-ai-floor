import random
from typing import List, Dict, Any
from jsonschema import validate, ValidationError
from app.executors.exercise_schema import exercise_schema

## pensar em implementar exames de salto na plataforma da Vald e usar para ML
class SerialBuilder:
    def __init__(self, exercise, athlete):
        self.exercise = exercise
        self.athlete = athlete
        
        self.parts_cmd = []
        self.command = ""
        
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

        print(self.parameters)

        self.validate_schema()
        self.validate_logic() 
        self.build_stimuli_sequence()
        self.build_delays()
        self.build_rounds()
        self.build()

        #self.validate_final_plan()

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
        self.parts_cmd.append("SET")
        stimuli_count = self.parameters["stimuli_count"]
        self.parts_cmd.append(str(stimuli_count))
        
        stimuli_generation_mode = self.parameters["stimuli_generation_mode"]
        if stimuli_generation_mode == "random":
            self.parts_cmd.append(str(0))

        """
        elif stimuli_generation_mode == "defined":
            sequence = self.parameters["stimuli_sequence"]
            if len(sequence) != stimuli_count:
                raise ValueError(
                    f"stimuli_sequence deve ter {stimuli_count} elementos, mas tem {len(sequence)}"
                )
        """
    
    def build_delays(self):
        delay_type = self.parameters["delay_type"]
        delay_range_ms = self.parameters["delay_range_ms"]
        #stimuli_count = self.parameters["stimuli_count"]

        if delay_type == "fixed":
            if len(delay_range_ms) != 1:
                raise ValueError("delay_range_ms deve ter 1 valor para delay_type='fixed'")
            self.parts_cmd.append(str(delay_range_ms[0]))
            
        """
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
        """

    def build_rounds(self):
        execution_rounds = self.parameters["execution_rounds"]
        self.parts_cmd.append(str(execution_rounds))

        if self.st_type == "color":
            correct_color = self.parameters.get("correct_color")
            self.parts_cmd.append(str(correct_color))

    def build(self):
        self.command = "|".join(self.parts_cmd) 

    
    def get_execution_plan(self):
        return self.command
    
    


