from __future__ import annotations

from typing import Dict, Type

from .base import Animation
from .bouncy_ball import BouncyBallAnimation

# For now, we'll create a simple placeholder for the ColorLayersAnimation
# In a real implementation, this would be a separate class
class ColorLayersAnimation(BouncyBallAnimation):
    pass

_REGISTRY: Dict[str, Type[Animation]] = {
    "ball": BouncyBallAnimation,
    "color": ColorLayersAnimation
}

def get_animation_class(name: str) -> Type[Animation]:
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
    _REGISTRY[name] = cls
