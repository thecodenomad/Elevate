# test_state_induction_controller.py
#
# Copyright 2025 thecodenomad
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

"""Unit tests for the StateInductionController class."""

import pytest
from gi.repository import GLib
from elevate.backend.state_induction_controller import StateInductionController
from elevate.settings import ElevateSettings

@pytest.fixture
def settings():
    """Fixture to create an ElevateSettings instance with a mock GSettings schema."""
    try:
        settings = ElevateSettings()
        print(settings.__dict__)
        return settings
    except GLib.Error as e:
        pytest.skip(f"GSettings schema not available: {e}")


def test_init(settings):
    """Test controller initialization."""
    controller = StateInductionController(settings)
    assert controller is not None
    assert controller.is_playing is False

def test_play(settings):
    """Test play functionality."""
    controller = StateInductionController(settings)
    controller.play()
    # Note: Actual audio/visual playback is not tested here
    # as it would require mocking the audio/visual components
    # and we're testing the controller logic only

def test_pause(settings):
    """Test pause functionality."""
    controller = StateInductionController(settings)
    controller.play()  # Start playing first
    controller.pause()
    assert controller.is_playing is False

def test_stop(settings):
    """Test stop functionality."""
    controller = StateInductionController(settings)
    controller.play()  # Start playing first
    controller.stop()
    assert controller.is_playing is False

def test_set_stimuli_type(settings):
    """Test setting stimuli type."""
    controller = StateInductionController(settings)
    # Test setting different stimuli types
    controller.stimuli_type = 0  # Color
    controller.stimuli_type = 1  # Breath Pattern
    # The actual effect is tested in visual_stimulus tests
