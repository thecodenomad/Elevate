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
from elevate.backend.state_induction_controller import StateInductionController


class TestStateInductionController:
    """Test suite for StateInductionController."""

    def test_init(self):
        """Test controller initialization."""
        controller = StateInductionController()
        assert controller is not None
        assert controller.get_is_playing() is False

    def test_play(self):
        """Test play functionality."""
        controller = StateInductionController()
        controller.play()
        # Note: Actual audio/visual playback is not tested here
        # as it would require mocking the audio/visual components
        # and we're testing the controller logic only

    def test_pause(self):
        """Test pause functionality."""
        controller = StateInductionController()
        controller.play()  # Start playing first
        controller.pause()
        assert controller.get_is_playing() is False

    def test_stop(self):
        """Test stop functionality."""
        controller = StateInductionController()
        controller.play()  # Start playing first
        controller.stop()
        assert controller.get_is_playing() is False

    def test_set_stimuli_type(self):
        """Test setting stimuli type."""
        controller = StateInductionController()
        # Test setting different stimuli types
        controller.set_stimuli_type(0)  # Color
        controller.set_stimuli_type(1)  # Breath Pattern
        # The actual effect is tested in visual_stimulus tests
