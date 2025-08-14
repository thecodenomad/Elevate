from unittest.mock import patch, MagicMock
from elevate.backend.animations import get_animation_class, register, _REGISTRY
from elevate.backend.animations.base import Animation
from elevate.backend.animations.bouncy_ball import BouncyBallAnimation


class TestAnimation(Animation):
    def reset(self):
        pass

    def update(self, dt: float, width: int, height: int) -> None:
        pass

    def render(self, cr, width: int, height: int, now_s: float) -> None:
        pass


def test_register_and_get_custom_animation():
    """Test registering a new animation type and retrieving it."""
    # Test registering a new animation without modifying global state
    with patch.dict(_REGISTRY, _REGISTRY.copy()) as mock_registry:
        # Register a new animation
        register("test", TestAnimation)
        
        # Retrieve the registered animation
        cls = get_animation_class("test")
        assert cls == TestAnimation


def test_get_animation_class_numeric_mappings():
    """Test all numeric mappings work correctly."""
    # Test all numeric mappings
    assert get_animation_class("0").__name__ == get_animation_class("color").__name__
    # For "1" -> "pulse", it should return BouncyBallAnimation as fallback
    assert get_animation_class("1").__name__ == BouncyBallAnimation.__name__
    assert get_animation_class("2").__name__ == get_animation_class("ball").__name__


def test_get_animation_class_case_insensitive():
    """Test that animation names are case insensitive."""
    assert get_animation_class("BALL").__name__ == get_animation_class("ball").__name__
    assert get_animation_class("COLOR").__name__ == get_animation_class("color").__name__


def test_get_animation_class_whitespace_stripped():
    """Test that whitespace is stripped from animation names."""
    assert get_animation_class(" ball ").__name__ == get_animation_class("ball").__name__
    assert get_animation_class(" color ").__name__ == get_animation_class("color").__name__