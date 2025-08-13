"""Constants module for Elevate application.

This module contains constants used throughout the Elevate application,
including brainwave state types and their frequency ranges.
"""

from enum import Enum

# TODO: This should be a part of the build pipeline
APPLICATION_ID = "org.thecodenomad.elevate"

LOWER_BOUND = "lower_bound"
UPPER_BOUND = "upper_bound"
DEFAULT = "default"
DESCRIPTION = "description"

class StateType(Enum):
    """Enumeration of brainwave state types and their frequency ranges."""

    DELTA = 0
    THETA = 1
    ALPHA = 2
    BETA = 3
    GAMMA = 4

STATE_TYPE_NAMES = ["Delta", "Theta", "Alpha", "Beta", "Gamma"]


# NOTE: Information obtained via Grok
# https://grok.com/share/bGVnYWN5_c323e05e-2640-4309-94c4-ea65c9259e01

# Bounding ranges for each state
# TODO: Maybe a classs instead?
STATE_DATA = {
    StateType.DELTA: {
        LOWER_BOUND: 0.3,
        UPPER_BOUND: 4.0,
        DEFAULT: 2.0,
        DESCRIPTION: (
            "Promotes profound relaxation and unconscious processes "
            "like physical recovery and immune function."
        )
    },
    StateType.THETA: {
        LOWER_BOUND: 4.1,
        UPPER_BOUND: 8.0,
        DEFAULT: 6.0,
        DESCRIPTION: (
            "Enhances intuition, emotional processing, "
            "and access to subconscious insights or vivid imagery."
        )
    },
    StateType.ALPHA: {
        LOWER_BOUND: 8.1,
        UPPER_BOUND: 13.0,
        DEFAULT: 10.0,
        DESCRIPTION: (
            "Boosts learning, stress relief, and a bridge between "
            "conscious and subconscious mind."
        )
    },
    StateType.BETA: {
        LOWER_BOUND: 13.1,
        UPPER_BOUND: 30.0,
        DEFAULT: 20.0,
        DESCRIPTION: (
            "Supports logical thinking, focus, and engagement in "
            "tasks requiring mental effort or decision-making."
        )
    },
    StateType.GAMMA: {
        LOWER_BOUND: 30.0,
        UPPER_BOUND: 130.0,
        DEFAULT: 40.0,
        DESCRIPTION: (
            "Linked to advanced learning, memory consolidation, "
            "and moments of clarity or inspiration."
        )
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
