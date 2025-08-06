import os
import importlib
import pytest


def test_settings_memory_defaults(conftest=None):
    from src.backend.elevate_settings import ElevateSettings
    s = ElevateSettings()
    assert s.get_base_frequency() == 200.0
    assert s.get_channel_offset() == 10.0
    assert s.get_enable_visual_stimuli() is False
    assert s.get_stimuli_type() == 0


def test_settings_roundtrip_setters():
    from src.backend.elevate_settings import ElevateSettings
    s = ElevateSettings()
    s.set_base_frequency(180.0)
    s.set_channel_offset(7.0)
    s.set_enable_visual_stimuli(True)
    s.set_stimuli_type(1)
    assert s.get_base_frequency() == 180.0
    assert s.get_channel_offset() == 7.0
    assert s.get_enable_visual_stimuli() is True
    assert s.get_stimuli_type() == 1
