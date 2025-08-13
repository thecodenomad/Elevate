from elevate.backend.animations import get_animation_class


def test_get_animation_class_case_and_strip_and_default():
    assert get_animation_class(" COLOR ").__name__
    # numeric map 0->color, 1->pulse, 2->ball
    assert get_animation_class("0").__name__ == get_animation_class("color").__name__
    assert get_animation_class("1").__name__ != get_animation_class("color").__name__
    assert get_animation_class("2").__name__ != get_animation_class("color").__name__
    # unknown returns default ColorLayersAnimation
    assert get_animation_class("nope").__name__ == get_animation_class("color").__name__
