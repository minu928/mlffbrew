import numpy as np
from typing import Iterable
from mlffbrew.mdpy.dataclasses import State, STATE_KEYS


def concatenate(states: Iterable[State]):
    assert all([isinstance(state, State) for state in states]), f"States are not isinstance of State."
    return State(**{key: np.concatenate([[getattr(state, key)] for state in states]) for key in STATE_KEYS})
