import os
import importlib
import pytest

from elevate.settings import ElevateSettings

# Defaults in the GSchema
def test_settings_memory_defaults(conftest=None):
    s = ElevateSettings()
    assert s.base_frequency == 30.0
    assert s.channel_offset == 6.0
    assert s.enable_visual_stimuli is True
    assert s.stimuli_type == 1


def test_settings_roundtrip_setters():
    s = ElevateSettings()
    s.base_frequency = 180.0
    s.channel_offset = 7.0
    s.enable_visual_stimuli = True
    s.stimuli_type = 2
    assert s.base_frequency == 180.0
    assert s.channel_offset == 7.0
    assert s.enable_visual_stimuli is True
    assert s.stimuli_type == 2
