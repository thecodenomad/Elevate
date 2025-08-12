# elevate_settings.py
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

"""Settings management for the Elevate application."""

from gi.repository import Gio, GObject


class ElevateSettings(GObject.Object):
    """Settings management for the Elevate application."""

    __gtype_name__ = "ElevateSettings"

    def __init__(self):
        """Initialize the settings manager."""
        super().__init__()
        self._settings = Gio.Settings.new("org.thecodenomad.elevate")

    @GObject.Property(type=float, default=200.0)
    def base_frequency(self):
        return self._settings.get_double("base-frequency")

    def get_base_frequency(self):
        return self.base_frequency

    def set_base_frequency(self, value):
        self.base_frequency = value

    @base_frequency.setter
    def base_frequency(self, value):
        """Set the base frequency setting."""
        self._settings.set_double("base-frequency", value)

    @GObject.Property(type=float, default=10.0)
    def channel_offset(self):
        return self._settings.get_double("channel-offset")

    def get_channel_offset(self):
        return self.channel_offset

    def set_channel_offset(self, value):
        self.channel_offset = value

    @channel_offset.setter
    def channel_offset(self, value):
        """Set the channel offset setting."""
        self._settings.set_double("channel-offset", value)

    @GObject.Property(type=bool, default=False)
    def enable_visual_stimuli(self):
        return self._settings.get_boolean("enable-visual-stimuli")

    def get_enable_visual_stimuli(self):
        return self.enable_visual_stimuli

    def set_enable_visual_stimuli(self, value):
        self.enable_visual_stimuli = value

    @enable_visual_stimuli.setter
    def enable_visual_stimuli(self, value):
        """Set whether visual stimuli are enabled."""
        self._settings.set_boolean("enable-visual-stimuli", value)

    @GObject.Property(type=int, default=0)
    def stimuli_type(self):
        return self._settings.get_int("stimuli-type")

    def get_stimuli_type(self):
        return self.stimuli_type

    def set_stimuli_type(self, value):
        self.stimuli_type = value

    @stimuli_type.setter
    def stimuli_type(self, value):
        """Set the type of visual stimuli to use."""
        self._settings.set_int("stimuli-type", value)

    def bind_property(self, source_prop, target, target_prop, flags):
        """Bind a settings property to a target property."""
        self._settings.bind(source_prop, target, target_prop, flags)
