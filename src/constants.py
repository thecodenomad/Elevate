from enum import Enum


class state_type(Enum):
    DELTA: 1
    THETA: 2
    ALPHA: 3
    BETA: 4
    GAMMA: 5


LOWER_BOUND = "lower_bound"
UPPER_BOUND = "upper_bound"

# Bounding ranges for each state
RANGES = {
    state_type.DELTA: {LOWER_BOUND: 0.3, UPPER_BOUND: 4.0},
    state_type.THETA: {LOWER_BOUND: 4.1, UPPER_BOUND: 8.0},
    state_type.ALPHA: {
        LOWER_BOUND: 8.1,
        UPPER_BOUND: 13.0,
    },
    state_type.BETA: {LOWER_BOUND: 13.1, UPPER_BOUND: 30.0},
    state_type.GAMMA: {LOWER_BOUND: 30.0, UPPER_BOUND: 130.0},
}
