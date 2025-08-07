from __future__ import annotations

from typing import Dict, Type

from .base import Animation
from .pulse import PulseAnimation
from .color_layers import ColorLayersAnimation
from .bouncy_ball import BouncyBallAnimation

_REGISTRY: Dict[str, Type[Animation]] = {
    "color": ColorLayersAnimation,
    "pulse": PulseAnimation,
    "ball": BouncyBallAnimation,
}


def get_animation_class(name: str) -> Type[Animation]:
    key = name.lower().strip()
    if key.isdigit():
        key = {"0": "color", "1": "pulse", "2": "ball"}.get(key, key)
    return _REGISTRY.get(key, ColorLayersAnimation) or ColorLayersAnimation


def register(name: str, cls: Type[Animation]) -> None:
    _REGISTRY[name] = cls
