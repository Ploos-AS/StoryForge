DEFAULT_MAX_STATES = 10_000


class StateSpaceLimitError(RuntimeError):
    def __init__(self, max_states: int):
        self.max_states = max_states
        super().__init__(f"state-space limit reached ({max_states} states)")
