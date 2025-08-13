# settings.py
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

"""Settings abstraction that wraps the GSchema for easily getting and saving
preference.
"""

from gi.repository import Gio, GObject
from elevate.constants import APPLICATION_ID

# pylint: disable=W0718

class ElevateSettings(GObject.Object):
    """Manages application settings using GSettings.

    This class provides properties to get and set application preferences and state,
    such as audio frequencies, session settings, and UI preferences, stored via GSettings.
    Changes are logged using the provided logger.
    """

    DEFAULT_EPILEPTIC_WARNING = True
    DEFAULT_LANGUAGE = 0
    DEFAULT_SESSION_LENGTH = 10
    DEFAULT_STATE = 0
    #    DEFAULT_VISUAL = "BouncyBall"
    #    DEFAULT_BREATH_TYPE = "4-7-8"

    DEFAULT_ENABLE_VISUAL = True
    DEFAULT_BASE_FREQUENCY = 30  # Restored to original value
    DEFAULT_SAVED_VOLUME = 25

    # Theta state default
    DEFAULT_STIMULI_TYPE = 1

    def __init__(self):
        """Initialize the settings with a GSettings instance and logger."""
        super().__init__()
        self.settings = Gio.Settings.new(APPLICATION_ID)

        # Debug logging for settings changes
        self.settings.connect("changed::base-frequency", self._on_base_frequency_changed)
        self.settings.connect("changed::channel-offset", self._on_channel_offset_changed)

    def _on_base_frequency_changed(self, settings, key):
        """Debug handler for base-frequency changes."""
        print(f"ElevateSettings: base-frequency changed to {settings.get_double(key)} Hz")

    def _on_channel_offset_changed(self, settings, key):
        """Debug handler for channel-offset changes."""
        print(f"ElevateSettings: channel-offset changed to {settings.get_double(key)} Hz")

    #################
    # Preferences   #
    #################

    @GObject.Property(type=float, default=30.0)
    def base_frequency(self) -> float:
        """The base frequency for audio stimuli.

        Returns:
            float: The base frequency in Hz (20-300 Hz range).
        """
        try:
            return self.settings.get_double("base-frequency")
        except Exception:
            return self.DEFAULT_BASE_FREQUENCY

    @base_frequency.setter
    def base_frequency(self, value: float) -> None:
        """Set the base frequency for audio stimuli.

        Args:
            value (float): The base frequency in Hz (20-300 Hz range).
        """
        self.settings.set_double("base-frequency", value)

    @GObject.Property(type=int, default=0)
    def intended_state(self) -> int:
        """The intended brainwave state.

        Returns:
            int: The intended state setting.
        """
        try:
            return self.settings.get_int("intended-state")
        except Exception:
            return self.DEFAULT_STATE

    @intended_state.setter
    def intended_state(self, value: int) -> None:
        """Set the intended brainwave state.

        Args:
            value (int): The intended state to set.
        """
        self.settings.set_int("intended-state", value)

    @GObject.Property(type=int, default=0)
    def session_length(self) -> int:
        """The length of a meditation session.

        Returns:
            int: The session length in minutes.
        """
        try:
            return self.settings.get_int("session-length")
        except Exception:
            return self.DEFAULT_SESSION_LENGTH

    @session_length.setter
    def session_length(self, value: int) -> None:
        """Set the length of a meditation session.

        Args:
            value (int): The session length in minutes.
        """
        self.settings.set_int("session-length", value)

    @GObject.Property(type=bool, default=True)
    def epileptic_warning(self) -> bool:
        """Whether to show the epileptic warning when starting a session.

        Returns:
            bool: True if the epileptic warning is enabled, False otherwise.
        """
        try:
            return self.settings.get_boolean("epileptic-warning")
        except Exception:
            return self.DEFAULT_EPILEPTIC_WARNING

    @epileptic_warning.setter
    def epileptic_warning(self, value: bool) -> None:
        """Set whether to show the epileptic warning.

        Args:
            value (bool): True to enable the warning, False to disable.
        """
        self.settings.set_boolean("epileptic-warning", value)

    @GObject.Property(type=int, default=0)
    def language(self) -> int:
        """The language/locale code for the user interface.

        Returns:
            int: The language setting (e.g., 'en').
        """
        try:
            return self.settings.get_int("language")
        except Exception:
            return self.DEFAULT_LANGUAGE

    @language.setter
    def language(self, value: int) -> None:
        """Set the language/locale code for the user interface.

        Args:
            value (int): The language code to set.
        """
        self.settings.set_int("language", value)

    #############################
    # Saved Application State   #
    #############################

    @GObject.Property(type=float, default=6.0)
    def channel_offset(self) -> float:
        """The channel offset for audio stimuli.

        Returns:
            float: The channel offset in Hz (1-20 Hz range).
        """
        try:
            return self.settings.get_double("channel-offset")
        except Exception:
            return 6.0

    @channel_offset.setter
    def channel_offset(self, value: float) -> None:
        """Set the channel offset for audio stimuli.

        Args:
            value (float): The channel offset in Hz (1-20 Hz range).
        """
        self.settings.set_double("channel-offset", value)

    @GObject.Property(type=bool, default=True)
    def enable_visual_stimuli(self) -> bool:
        """Whether to enable visual stimuli for mental state induction.

        Returns:
            bool: True if visual stimuli are enabled, False otherwise.
        """
        try:
            return self.settings.get_boolean("enable-visual-stimuli")
        except Exception:
            return self.DEFAULT_ENABLE_VISUAL

    @enable_visual_stimuli.setter
    def enable_visual_stimuli(self, value: bool) -> None:
        """Set whether to enable visual stimuli.

        Args:
            value (bool): True to enable visual stimuli, False to disable.
        """
        self.settings.set_boolean("enable-visual-stimuli", value)

    @property
    def saved_volume(self) -> int:
        """The last volume used state.

        Returns:
            int: The saved volume setting.
        """
        try:
            return self.settings.get_int("saved-volume")
        except Exception:
            return self.DEFAULT_SAVED_VOLUME

    @saved_volume.setter
    def saved_volume(self, value: int) -> None:
        """Set the last volume used state.

        Args:
            value (int): The volume to set.
        """
        self.settings.set_int("saved-volume", value)

    @GObject.Property(type=int, default=0)
    def stimuli_type(self) -> int:
        """The type of visual stimuli to use.

        Returns:
            int: The stimuli type (e.g., 0 for color, 1 for breath patterns).
        """
        try:
            return self.settings.get_int("stimuli-type")
        except Exception:
            return self.DEFAULT_STIMULI_TYPE

    @stimuli_type.setter
    def stimuli_type(self, value: int) -> None:
        """Set the type of visual stimuli.

        Args:
            value (int): The stimuli type to set (e.g., 0 for color, 1 for breath patterns).
        """
        self.settings.set_int("stimuli-type", value)
