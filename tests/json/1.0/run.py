import jsonschema
from jsonschema import validate, ValidationError

exercise_schema = {
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
                    "description": "Number of distractor colors to light up along with the correct color."
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



sample_tests = []

# 1. Teste mínimo, sequência definida simples
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 3,
        "stimuli_generation_mode": "defined",
        "stimuli_sequence": [1, 2, 3],
        "stimulus_type": "color",
        "correct_color": "green",
        "delay_type": "fixed",
        "delay_range_ms": [500],
        "execution_rounds": 1
    }
})  # Simple test with 3 stimuli, fixed delay, single round

# 2. Teste com múltiplos rounds
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 5,
        "stimuli_generation_mode": "random",
        "stimuli_sequence": [],
        "stimulus_type": "color",
        "correct_color": "red",
        "delay_type": "fixed",
        "delay_range_ms": [600],
        "execution_rounds": 3
    }
})  # Randomized sequence, 3 rounds

# 3. Teste com distractor aleatório
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 6,
        "stimuli_generation_mode": "adaptive",
        "stimuli_sequence": list(range(1, 7)),
        "stimulus_type": "color",
        "correct_color": "#00FF00",
        "distractor_type": "color",
        "distractor_colors": ["red"],
        "distractor_ncolors_at_time": 2,
        "delay_type": "individual",
        "delay_range_ms": [200, 400, 600, 800, 1000, 1200],
        "execution_rounds": 2
    }
})  # Adaptive test with 2 distractors per stimulus

# 4. Teste de posição
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 4,
        "stimuli_generation_mode": "pattern_based",
        "stimuli_sequence": [1, 3, 2, 4],
        "stimulus_type": "position",
        "correct_color": "blue",
        "delay_type": "fixed",
        "delay_range_ms": [700],
        "execution_rounds": 1
    }
})  # Position-based stimulus, fixed delay

# 5. Teste multi_light
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 5,
        "stimuli_generation_mode": "defined",
        "stimuli_sequence": [1, 2, 3, 4, 5],
        "stimulus_type": "multi_light",
        "correct_color": "yellow",
        "delay_type": "fixed",
        "delay_range_ms": [500],
        "execution_rounds": 2
    }
})  # Multiple lights on at once

# 6. Teste fake_light
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 4,
        "stimuli_generation_mode": "random",
        "stimuli_sequence": [],
        "stimulus_type": "fake_light",
        "correct_color": "green",
        "delay_type": "range",
        "delay_range_ms": [300, 800],
        "execution_rounds": 1
    }
})  # Fake light test with variable delay

# 7. Teste timed
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 3,
        "stimuli_generation_mode": "defined",
        "stimuli_sequence": [1, 2, 3],
        "stimulus_type": "timed",
        "correct_color": "red",
        "delay_type": "fixed",
        "delay_range_ms": [400],
        "execution_rounds": 2,
        "timeout_ms": 1000
    }
})  # Stimulus requires quick response (timeout applied)

# 8. Teste pattern
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 6,
        "stimuli_generation_mode": "pattern_based",
        "stimuli_sequence": [1, 2, 3, 4, 5, 6],
        "stimulus_type": "pattern",
        "correct_color": "blue",
        "delay_type": "fixed",
        "delay_range_ms": [500],
        "execution_rounds": 1
    }
})  # Defined pattern sequence

# 9. Teste com hexadecimal
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 4,
        "stimuli_generation_mode": "random",
        "stimuli_sequence": [],
        "stimulus_type": "color",
        "correct_color": "#123ABC",
        "delay_type": "fixed",
        "delay_range_ms": [600],
        "execution_rounds": 1
    }
})  # Color test using hex code

# 10. Teste complexo com rounds e distractors
sample_tests.append({
    "category": "Performance",
    "modality": "Single-Touch",
    "parameters": {
        "stimuli_count": 8,
        "stimuli_generation_mode": "adaptive",
        "stimuli_sequence": list(range(1, 9)),

        "stimulus_type": "color",
        "correct_color": "yellow",

        "distractor_type": "color",
        "distractor_colors": ["red", "blue", "green"],
        "distractor_ncolors_at_time": 2,
        
        "delay_type": "individual",
        "delay_range_ms": [100, 300, 500, 700, 900, 1100, 1300, 1500],
        "execution_rounds": 3
    }
})  # Adaptive test with multiple distractors and multiple rounds



for i, test_json in enumerate(sample_tests, start=1):
    print(f"\n=== Test {i} ===")
    try:
        validate(instance=test_json, schema=exercise_schema)
        print("✅ Validation passed")
    except ValidationError as e:
        print(f"❌ Validation failed: {e.message}")




