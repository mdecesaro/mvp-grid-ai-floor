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