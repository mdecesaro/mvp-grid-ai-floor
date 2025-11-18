from datetime import datetime

class EvaluationTest:
    def __init__(
        self,
        id=None,
        athlete_id=None,
        exercise_id=None,
        device_id=None,
        platform_version=None,
        timestamp=None,
        stimuli_count=0,
        delay_type="",
        delay_min_ms=0,
        delay_max_ms=0,
        execution_rounds=0,
        timeout_ms=0,
        repeat_if_wrong=False,
        total_attempts=0,
        hits=0,
        errors=0,
        avg_reaction_time=0.0,
        duration_ms=0,
        results=None
    ):
        self.id = id
        self.athlete_id = athlete_id
        self.exercise_id = exercise_id
        self.device_id = device_id
        self.platform_version = platform_version
        # ISO 8601 (YYYY-MM-DDTHH:MM:SS)
        self.timestamp = timestamp or datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.stimuli_count = stimuli_count
        self.delay_type = delay_type
        self.delay_min_ms = delay_min_ms
        self.delay_max_ms = delay_max_ms
        self.execution_rounds = execution_rounds
        self.timeout_ms = timeout_ms
        self.repeat_if_wrong = bool(repeat_if_wrong)
        self.total_attempts = total_attempts
        self.hits = hits
        self.errors = errors
        self.avg_reaction_time = avg_reaction_time
        self.duration_ms = duration_ms
        self.results = results or []
        
    def __repr__(self):
        return (
            f"Test(id={self.id}, athlete_id={self.athlete_id}, exercise_id={self.exercise_id}, "
            f"device_id='{self.device_id}', platform_version='{self.platform_version}', "
            f"timestamp='{self.timestamp}', stimuli_count={self.stimuli_count}, delay_type='{self.delay_type}', "
            f"delay_min_ms={self.delay_min_ms}, delay_max_ms={self.delay_max_ms}, execution_rounds={self.execution_rounds}, "
            f"timeout_ms={self.timeout_ms}, repeat_if_wrong={self.repeat_if_wrong}, total_attempts={self.total_attempts}, "
            f"hits={self.hits}, errors={self.errors}, avg_reaction_time={self.avg_reaction_time}, "
            f"duration_ms={self.duration_ms})"
        )

    @classmethod
    def from_row(cls, row):
        return cls(
            id=row["id"],
            athlete_id=row["athlete_id"],
            exercise_id=row["exercise_id"],
            device_id=row["device_id"] if "device_id" in row.keys() else None,
            platform_version=row["platform_version"] if "platform_version" in row.keys() else None,
            timestamp=row["timestamp"],
            stimuli_count=row["stimuli_count"],
            delay_type=row["delay_type"],
            delay_min_ms=row["delay_min_ms"],
            delay_max_ms=row["delay_max_ms"],
            execution_rounds=row["execution_rounds"],
            timeout_ms=row["timeout_ms"],
            repeat_if_wrong=bool(row["repeat_if_wrong"]),
            total_attempts=row["total_attempts"],
            hits=row["hits"],
            errors=row["errors"],
            avg_reaction_time=row["avg_reaction_time"],
            duration_ms=row["duration_ms"] if "duration_ms" in row.keys() else 0
        )

