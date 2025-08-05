# test_visual_stimulus.py
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

"""Unit tests for the VisualStimulus class."""

import pytest
from src.backend.visual_stimulus import VisualStimulus


class TestVisualStimulus:
    """Test suite for VisualStimulus."""

    def test_init(self):
        """Test visual stimulus initialization."""
        visual = VisualStimulus()
        assert visual is not None
        assert visual.get_enable_visual_stimuli() is False
        assert visual.get_stimuli_type() == 0

    def test_set_enable_visual_stimuli(self):
        """Test enabling visual stimuli."""
        visual = VisualStimulus()
        visual.set_enable_visual_stimuli(True)
        assert visual.get_enable_visual_stimuli() is True

    def test_set_stimuli_type(self):
        """Test setting stimuli type."""
        visual = VisualStimulus()
        visual.set_stimuli_type(1)  # Breath Pattern
        assert visual.get_stimuli_type() == 1

    def test_play(self):
        """Test play functionality."""
        visual = VisualStimulus()
        visual.set_enable_visual_stimuli(True)
        visual.play()
        # Note: We're not actually testing visual rendering here
        # as it would require a GUI environment. We're testing
        # the state management.

    def test_pause(self):
        """Test pause functionality."""
        visual = VisualStimulus()
        visual.set_enable_visual_stimuli(True)
        visual.play()
        visual.pause()
        assert visual._is_playing is False

    def test_stop(self):
        """Test stop functionality."""
        visual = VisualStimulus()
        visual.set_enable_visual_stimuli(True)
        visual.play()
        visual.stop()
        assert visual._is_playing is False

    def test_set_widget(self):
        """Test setting widget."""
        visual = VisualStimulus()
        # Create a mock widget
        class MockWidget:
            pass
        
        widget = MockWidget()
        visual.set_widget(widget)
        assert visual._widget == widget