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

import time

from gi.repository import GObject, Gio
from elevate.backend.audio_stimulus import AudioStimulus
from elevate.backend.visual_stimulus import VisualStimulus
from elevate.settings import ElevateSettings


class StateInductionController(GObject.Object):
    """Controller for managing mental state induction workflow."""

    def __init__(self):
        """Initialize the state induction controller.

        Sets up audio/visual stimuli interfaces, connects property bindings, and initializes
        state tracking attributes. Creates fresh stimulus instances for each controller.

        Raises:
            RuntimeError: If system resources are unavailable for stimulus creation
        """
        super().__init__()
        self._settings = ElevateSettings()
        self.audio_stimulus = AudioStimulus()
        self.visual_stimulus = VisualStimulus()
        self._is_playing = False
        self._is_paused = False
        self._elapsed_time = None
        self._start_time = None

        # Bind settings to audio stimulus using Gio.Settings.bind
        self._settings.app_config.bind(
            "base-frequency",
            self.audio_stimulus,
            "base-frequency",
            Gio.SettingsBindFlags.DEFAULT | Gio.SettingsBindFlags.GET | Gio.SettingsBindFlags.SET,
        )
        self._settings.app_config.bind(
            "channel-offset",
            self.audio_stimulus,
            "channel-offset",
            Gio.SettingsBindFlags.DEFAULT | Gio.SettingsBindFlags.GET | Gio.SettingsBindFlags.SET,
        )

        # Bind settings to visual stimulus using Gio.Settings.bind
        self._settings.app_config.bind(
            "enable-visual-stimuli",
            self.visual_stimulus,
            "enable-visual-stimuli",
            Gio.SettingsBindFlags.DEFAULT | Gio.SettingsBindFlags.GET | Gio.SettingsBindFlags.SET,
        )
        self._settings.app_config.bind(
            "stimuli-type",
            self.visual_stimulus,
            "stimuli-type",
            Gio.SettingsBindFlags.DEFAULT | Gio.SettingsBindFlags.GET | Gio.SettingsBindFlags.SET,
        )

        # Debug logging for settings changes
        self._settings.connect("notify::base-frequency", self._on_settings_base_frequency_changed)
        self._settings.connect("notify::channel-offset", self._on_settings_channel_offset_changed)

    def _on_settings_base_frequency_changed(self, obj, pspec):
        """Debug handler for settings base-frequency changes."""
        print(
            f"StateInductionController: settings.base-frequency changed to {self._settings.base_frequency} Hz"
        )

    def _on_settings_channel_offset_changed(self, obj, pspec):
        """Debug handler for settings channel-offset changes."""
        print(
            f"StateInductionController: settings.channel-offset changed to {self._settings.channel_offset} Hz"
        )

    @GObject.Property(type=bool, default=False)
    def is_playing(self):
        return self._is_playing

    def get_is_playing(self):
        return self.is_playing

    @GObject.Property(type=bool, default=False)
    def is_paused(self):
        """Check if playback is paused.

        Returns:
            bool: True if playback is paused, False otherwise
        """
        return self._is_paused

    @GObject.Property(type=float, default=False)
    def elapsed_time(self):
        """Get the total elapsed time of playback in seconds.

        Returns:
            float: Total time in seconds since playback started, adjusted for pauses
            Returns 0.0 if playback has never been initiated
        """

        elapsed_time = self._elapsed_time or 0.0
        if self._start_time is None:
            return elapsed_time

        elapsed_time += time.monotonic() - self._start_time
        return elapsed_time

    def play(self):
        """Start audio/visual stimuli playback and reset elapsed time tracking.

        Starts both audio and visual stimuli if not already playing, captures start time
        for tracking playback duration, and updates internal state flags.

        Raises:
            RuntimeError: If stimuli playback interfaces are not properly initialized
        """
        if not self._is_playing:
            self.audio_stimulus.play()
            if self._settings.enable_visual_stimuli:
                self.visual_stimulus.play()
            self._is_playing = True

            # capture start time
            self._start_time = time.monotonic()

            self.notify("is-playing")
            self._is_paused = False

    def pause(self):
        """Pause all active audio/visual stimuli and update tracking state.

        Stops playback without resetting elapsed time counters, preserving playback position.
        Only effective if currently playing (is_playing is True).

        Raises:
            RuntimeError: If stimuli interfaces are not properly initialized
        """
        if self._is_playing:
            self.audio_stimulus.pause()
            self.visual_stimulus.pause()
            self._is_playing = False
            self.notify("is-playing")
            self._is_paused = True

    def stop(self):
        """Halt all active stimuli and finalize elapsed time tracking.

        Stops both audio and visual stimuli immediately and updates internal state.
        Finalizes the elapsed time counter by adding the duration since last start.

        Raises:
            RuntimeError: If stimuli interfaces are not properly initialized
        """
        self.audio_stimulus.stop()
        self.visual_stimulus.stop()
        self._is_playing = False
        self._is_paused = False

        if self._start_time is not None:
            if self._elapsed_time is None:
                self._elapsed_time = time.monotonic() - self._start_time
            else:
                self._elapsed_time += time.monotonic() - self._start_time
            self._start_time = None

        self.notify("is-playing")

    def set_stimuli_type(self, stimuli_type):
        """Configure the visual stimulus pattern type.

        Args:
            stimuli_type (int): Index of the stimulus type to activate

        Raises:
            ValueError: If the stimulus type index is out of range
            RuntimeError: If visual stimulus interface not initialized
        """
        self.visual_stimulus.set_stimuli_type(stimuli_type)
