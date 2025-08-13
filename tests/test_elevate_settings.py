# tests/test_elevate_settings.py
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

import pytest
from gi.repository import Gio, GLib
from elevate.settings import ElevateSettings
from elevate.constants import APPLICATION_ID


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
    """Test settings initialization."""
    assert settings is not None
    # Test default values from schema
    assert settings.base_frequency == 30.0
    assert settings.channel_offset == 6.0
    assert settings.intended_state == 0
    assert settings.session_length == 10
    assert settings.epileptic_warning is True
    assert settings.language == 0
    assert settings.enable_visual_stimuli is True
    assert settings.saved_volume == 25
    assert settings.stimuli_type == 1


def test_base_frequency_set_get(settings):
    """Test setting and getting base_frequency."""
    settings.base_frequency = 100.0
    assert settings.base_frequency == 100.0
    # Test out-of-range values
    settings.base_frequency = 400.0
    assert settings.base_frequency == 300.0  # Clamped to max
    settings.base_frequency = 10.0
    assert settings.base_frequency == 20.0  # Clamped to min


def test_channel_offset_set_get(settings):
    """Test setting and getting channel_offset."""
    settings.channel_offset = 15.0
    assert settings.channel_offset == 15.0
    # Test out-of-range values
    settings.channel_offset = 125.0
    assert settings.channel_offset == 100.0  # Clamped to max
    settings.channel_offset = 0.5
    assert settings.channel_offset == 1.0  # Clamped to min
