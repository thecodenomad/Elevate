# test_audio_stimulus.py
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

"""Unit tests for the AudioStimulus class."""

import pytest
from elevate.backend.audio_stimulus import AudioStimulus


class TestAudioStimulus:
    """Test suite for AudioStimulus."""

    def test_init(self):
        """Test audio stimulus initialization."""
        audio = AudioStimulus()
        assert audio is not None
        assert audio.base_frequency == 200.0
        assert audio.channel_offset == 10.0

    def test_set_base_frequency(self):
        """Test setting base frequency."""
        audio = AudioStimulus()
        audio.base_frequency = 150.0
        assert audio.base_frequency == 150.0

    def test_set_channel_offset(self):
        """Test setting channel offset."""
        audio = AudioStimulus()
        audio.channel_offset = 5.0
        assert audio.channel_offset == 5.0

    def test_play(self):
        """Test play functionality."""
        audio = AudioStimulus()
        # Note: We're not actually testing audio playback here
        # as it would require mocking the GStreamer library
        # and hardware access. We're testing the state management.
        audio.play()
        # The actual stream is tested in integration tests

    def test_pause(self):
        """Test pause functionality."""
        audio = AudioStimulus()
        audio.play()
        audio.pause()
        # The actual stream is tested in integration tests

    def test_stop(self):
        """Test stop functionality."""
        audio = AudioStimulus()
        audio.play()
        audio.stop()
        # The actual stream is tested in integration tests