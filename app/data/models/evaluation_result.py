class EvaluationResult:
    def __init__(
        self,
        id=None,
        test_id=None,
        round_num=0,
        stimulus_id=None,
        stimulus_position=None,
        stimulus_type=None,
        correct_color=None,
        reaction_time=None,
        stimulus_start=None,
        stimulus_end=None,
        delay_ms=None,
        elapsed_since_start=None,
        error=False,
        foot_used=None,
        wrong_stimulus_id=None,
        distractor_type=None,
        distractor_id_color=None
        
    ):
        self.id = id
        self.test_id = test_id
        self.round_num = round_num
        self.stimulus_id = stimulus_id
        self.stimulus_position = stimulus_position
        self.stimulus_type = stimulus_type
        self.correct_color = correct_color
        self.reaction_time = reaction_time
        self.stimulus_start = stimulus_start
        self.stimulus_end = stimulus_end
        self.delay_ms = delay_ms
        self.elapsed_since_start = elapsed_since_start
        self.error = bool(error)
        self.foot_used = foot_used
        self.wrong_stimulus_id = wrong_stimulus_id
        self.distractor_type = distractor_type
        self.distractor_id_color = distractor_id_color or []
        

    def __repr__(self):
        return (
            f"TestResult(id={self.id}, test_id={self.test_id}, round_num={self.round_num}, "
            f"stimulus_id={self.stimulus_id}, stimulus_position={self.stimulus_position}, "
            f"stimulus_type={self.stimulus_type}, reaction_time={self.reaction_time}, "
            f"stimulus_start={self.stimulus_start}, "
            f"stimulus_end={self.stimulus_end}, delay_ms={self.delay_ms}, correct_color={self.correct_color}, "
            f"error={self.error}, foot_used={self.foot_used}, wrong_stimulus_id={self.wrong_stimulus_id}, "
            f"distractor_type={self.distractor_type}, distractor_id_color={self.distractor_id_color}, "
            f"elapsed_since_start={self.elapsed_since_start})"
        )

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=data.get("id"),
            test_id=data.get("test_id"),
            round_num=data.get("round_num", 0),
            stimulus_id=data.get("stimulus_id"),
            stimulus_position=data.get("stimulus_position"),
            stimulus_type=data.get("stimulus_type"),
            reaction_time=data.get("reaction_time"),
            stimulus_start=data.get("stimulus_start"),
            stimulus_end=data.get("stimulus_end"),
            delay_ms=data.get("delay_ms"),
            correct_color=data.get("correct_color"),
            error=data.get("error", False),
            foot_used=data.get("foot_used"),
            wrong_stimulus_id=data.get("wrong_stimulus_id"),
            distractor_type=data.get("distractor_type"),
            distractor_id_color=data.get("distractor_id_color", []),
            elapsed_since_start=data.get("elapsed_since_start")
        )
