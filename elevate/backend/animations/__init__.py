"""
Animation framework for visual stimuli in the Elevate application.

This module provides the infrastructure for managing different animation types
used in visual stimuli. It includes base classes, concrete implementations,
and a registry system for animation types.
"""

from __future__ import annotations

from typing import Dict, Type

from .base import Animation
from .bouncy_ball import BouncyBallAnimation


class ColorLayersAnimation(BouncyBallAnimation):
    """Placeholder implementation for color layer animations.

    Note:
        This is currently a placeholder that inherits from BouncyBallAnimation.
        A proper implementation will be added in future versions.
    """

    pass


_REGISTRY: Dict[str, Type[Animation]] = {
    "ball": BouncyBallAnimation,
    "color": ColorLayersAnimation,
}


def get_animation_class(name: str) -> Type[Animation]:
    """Retrieve an animation class by name or numeric identifier.

    Supports both string names ('ball', 'color') and numeric identifiers
    (0=color, 1=pulse, 2=ball) for compatibility with UI settings.

    Args:
        name: Animation identifier as string or number

    Returns:
        Animation class type, falling back to ColorLayersAnimation if not found
    """
    key = name.lower().strip()
    # Numeric mapping per test requirements:
    # 0->color, 1->pulse (placeholder), 2->ball
    key_map = {"0": "color", "1": "pulse", "2": "ball"}
    mapped_key = key_map.get(key, key)

    # Handle special case for pulse (not yet implemented)
    if mapped_key == "pulse":
        return BouncyBallAnimation  # Temporary, would be different in full implementation

    return _REGISTRY.get(mapped_key, ColorLayersAnimation)


def register(name: str, cls: Type[Animation]) -> None:
    """Register a new animation class with the system.

    Args:
        name: Identifier for the animation
        cls: Animation class to register
    """
    _REGISTRY[name] = cls
