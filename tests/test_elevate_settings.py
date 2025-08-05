# test_elevate_settings.py
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

"""Unit tests for the ElevateSettings class."""

import pytest
from src.backend.elevate_settings import ElevateSettings


class TestElevateSettings:
    """Test suite for ElevateSettings."""

    def test_init(self):
        """Test settings initialization."""
        settings = ElevateSettings()
        assert settings is not None
        # Test default values from schema
        assert settings.get_base_frequency() == 200.0
        assert settings.get_channel_offset() == 10.0
        assert settings.get_enable_visual_stimuli() is False
        assert settings.get_stimuli_type() == 0

    def test_set_base_frequency(self):
        """Test setting base frequency."""
        settings = ElevateSettings()
        settings.set_base_frequency(150.0)
        assert settings.get_base_frequency() == 150.0

    def test_set_channel_offset(self):
        """Test setting channel offset."""
        settings = ElevateSettings()
        settings.set_channel_offset(5.0)
        assert settings.get_channel_offset() == 5.0

    def test_set_enable_visual_stimuli(self):
        """Test enabling visual stimuli."""
        settings = ElevateSettings()
        settings.set_enable_visual_stimuli(True)
        assert settings.get_enable_visual_stimuli() is True

    def test_set_stimuli_type(self):
        """Test setting stimuli type."""
        settings = ElevateSettings()
        settings.set_stimuli_type(1)
        assert settings.get_stimuli_type() == 1

    def test_bind_property(self):
        """Test property binding.
        
        Note: This is a basic test of the binding mechanism.
        Actual binding functionality is tested in integration tests.
        """
        settings = ElevateSettings()
        # Test that the method exists and can be called
        # The actual binding is tested with real GObject objects
        assert hasattr(settings, 'bind_property')