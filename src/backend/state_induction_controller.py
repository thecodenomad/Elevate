# state_induction_controller.py
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

"""Controller for managing mental state induction workflow."""

from gi.repository import GObject, Gio
from .audio_stimulus import AudioStimulus
from .visual_stimulus import VisualStimulus
from .elevate_settings import ElevateSettings


class StateInductionController(GObject.Object):
    """Controller for managing mental state induction workflow."""

    def __init__(self):
        """Initialize the controller."""
        super().__init__()
        self._settings = ElevateSettings()
        self._audio_stimulus = AudioStimulus()
        self._visual_stimulus = VisualStimulus()
        self._is_playing = False
        self._is_paused = False

        # Bind settings to audio stimulus
        self._settings.bind_property(
            "base-frequency",
            self._audio_stimulus,
            "base-frequency",
            GObject.BindingFlags.DEFAULT
        )
        self._settings.bind_property(
            "channel-offset",
            self._audio_stimulus,
            "channel-offset",
            GObject.BindingFlags.DEFAULT
        )

        # Bind settings to visual stimulus
        self._settings.bind_property(
            "enable-visual-stimuli",
            self._visual_stimulus,
            "enable-visual-stimuli",
            GObject.BindingFlags.DEFAULT
        )
        self._settings.bind_property(
            "stimuli-type",
            self._visual_stimulus,
            "stimuli-type",
            GObject.BindingFlags.DEFAULT
        )

    @GObject.Property(type=bool, default=False)
    def is_playing(self):
        """Get whether stimuli are currently playing."""
        return self._is_playing

    @GObject.Property(type=bool, default=False)
    def is_paused(self):
        """Get whether stimuli are currently playing."""
        return self._is_paused

    def play(self):
        """Start playing audio and visual stimuli."""
        if not self._is_playing:
            self._audio_stimulus.play()
            if self._settings.enable_visual_stimuli:
                self._visual_stimulus.play()
            self._is_playing = True
            self.notify("is-playing")
            self._is_paused = False

    def pause(self):
        """Pause audio and visual stimuli."""
        if self._is_playing:
            self._audio_stimulus.pause()
            self._visual_stimulus.pause()
            self._is_playing = False
            self.notify("is-playing")
            self._is_paused = True

    def stop(self):
        """Stop audio and visual stimuli."""
        self._audio_stimulus.stop()
        self._visual_stimulus.stop()
        self._is_playing = False
        self._is_paused = False
        self.notify("is-playing")

    def set_stimuli_type(self, stimuli_type):
        """Set the type of visual stimuli to use."""
        self._visual_stimulus.set_stimuli_type(stimuli_type)
