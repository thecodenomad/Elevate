"""Constants module for Elevate application.

This module contains constants used throughout the Elevate application,
including brainwave state types and their frequency ranges.
"""

from enum import Enum

LOWER_BOUND = "lower_bound"
UPPER_BOUND = "upper_bound"
DEFAULT = "default"

class StateType(Enum):
    """Enumeration of brainwave state types and their frequency ranges."""

    DELTA = 0
    THETA = 1
    ALPHA = 2
    BETA = 3
    GAMMA = 5

STATE_TYPE_NAMES = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]

# Bounding ranges for each state
RANGES = {
    StateType.DELTA: {
        LOWER_BOUND: 0.3,
        UPPER_BOUND: 4.0,
        DEFAULT: 2.0,
    },
    StateType.THETA: {
        LOWER_BOUND: 4.1,
        UPPER_BOUND: 8.0,
        DEFAULT: 6.0
    },
    StateType.ALPHA: {
        LOWER_BOUND: 8.1,
        UPPER_BOUND: 13.0,
        DEFAULT: 10.0
    },
    StateType.BETA: {
        LOWER_BOUND: 13.1,
        UPPER_BOUND: 30.0,
        DEFAULT: 20.0
    },
    StateType.GAMMA: {
        LOWER_BOUND: 30.0,
        UPPER_BOUND: 130.0,
        DEFAULT: 40.0
    }
}

LANGUAGE_CODES = [
    "en",
    "zh_CN",
    "es",
    "hi",
    "ar",
    "pt",
    "fr",
    "bn",
    "ru",
    "ja",
    "ta",
    "te",
    "pa",
    "id",
    "vi",
    "sw",
    "th",
]

LANGUAGES = [
    "English",
    "Mandarin Chinese",
    "Spanish",
    "Hindi",
    "Arabic",
    "Portuguese",
    "French",
    "Bengali",
    "Russian",
    "Japanese",
    "Tamil",
    "Telugu",
    "Punjabi",
    "Indonesian",
    "Vietnamese",
    "Swahili",
    "Thai"
]
