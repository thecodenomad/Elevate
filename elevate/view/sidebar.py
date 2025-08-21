# sidebar.py
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

"""Control sidebar for the Elevate application."""

import gi

gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GObject

# Import constants using relative import
from elevate.constants import (
    DEFAULT,
    LOWER_BOUND,
    UPPER_BOUND,
    STATE_DATA,
    StateType,
    STATE_FUNC_NAMES,
    STATE_TYPE_NAMES,
)

# pylint: disable=E1101


@Gtk.Template(resource_path="/org/thecodenomad/elevate/sidebar.ui")
class Sidebar(Gtk.Box):
    """Control sidebar for the Elevate application."""

    __gtype_name__ = "Sidebar"

    intended_state_combo = Gtk.Template.Child()
    minutes_spin_button = Gtk.Template.Child()
    advanced_settings_switch = Gtk.Template.Child()
    intended_state_combo = Gtk.Template.Child()

    advanced_audio_settings = Gtk.Template.Child()
    # TODO: Not supported yet
    # advanced_visual_settings = Gtk.Template.Child()

    frequency_scale = Gtk.Template.Child()
    channel_offset_scale = Gtk.Template.Child()
    visual_stimuli_switch = Gtk.Template.Child()
    # TODO: Not supported yet
    # stimuli_type_combo = Gtk.Template.Child()

    def __init__(self, controller, settings, **kwargs):
        """Initialize the sidebar."""
        super().__init__(**kwargs)
        self.state_handler_id = None
        self.offset_handler_id = None
        self.controller = controller
        self.settings = settings

        string_list = Gtk.StringList.new(STATE_FUNC_NAMES)
        self.intended_state_combo.set_model(string_list)

        self.set_bindings()

    def set_defaults(self):
        """Helper method to load saved settings into the sidebar widgets."""
        # Block the channel_offset_scale signal to prevent unwanted updates

        GObject.signal_handler_block(self.channel_offset_scale, self.offset_handler_id)
        GObject.signal_handler_block(self.intended_state_combo, self.state_handler_id)

        # Set Intended State
        state_idx = self.settings.intended_state
        state_type = list(StateType)[state_idx]
        self.intended_state_combo.set_selected(state_idx)

        tooltip = (
                    f"{state_type.name}: {STATE_DATA[state_type][LOWER_BOUND]} "
                    f"to {STATE_DATA[state_type][UPPER_BOUND]} Hz - {STATE_DATA[state_type]['description']}"
                )
        self.intended_state_combo.set_tooltip_text(tooltip)
        self.intended_state_combo.set_title(
            f"{STATE_TYPE_NAMES[state_idx]} ({STATE_DATA[state_type][DEFAULT]} Hz)"
        )

        # Set Default Channel Offset
        default_offset = STATE_DATA[state_type][DEFAULT]
        self.channel_offset_scale.set_value(default_offset)

        # Set Default Session Length
        session_length = self.settings.session_length
        self.minutes_spin_button.set_value(session_length)

        # Set Default Base Frequency
        base_frequency = self.settings.base_frequency
        self.frequency_scale.set_value(base_frequency)

        # Set Enable Visual Stimuli
        enable_visuals = self.settings.enable_visual_stimuli
        self.visual_stimuli_switch.set_active(enable_visuals)

        # Unblock the channel_offset_scale signal
        GObject.signal_handler_unblock(self.channel_offset_scale, self.offset_handler_id)
        GObject.signal_handler_unblock(self.intended_state_combo, self.state_handler_id)

    def on_intended_state_combo_changed(self, combo, _pspec):
        """Handle changes to the intended_state_combo.

        When a user selects a state from the combo box, this method will:
        1. Map the selection to a StateType enum
        2. Set the channel_offset_scale to the default value for that state
        3. Update the settings with the new intended state
        """

        selected_index = combo.get_selected()
        if selected_index != Gtk.INVALID_LIST_POSITION:

            # Map the index to the StateType enum
            try:
                state_type = list(StateType)[selected_index]
                # Set the channel_offset_scale to the default value for this state
                default_value = STATE_DATA[state_type][DEFAULT]
                tooltip = (
                    f"{state_type.name}: {STATE_DATA[state_type][LOWER_BOUND]} "
                    f"to {STATE_DATA[state_type][UPPER_BOUND]} Hz - {STATE_DATA[state_type]['description']}"
                )
                combo.set_tooltip_text(tooltip)
                combo.set_title(
                    f"{STATE_TYPE_NAMES[selected_index]} ({STATE_DATA[state_type][DEFAULT]} Hz)"
                )

                adjustment = self.channel_offset_scale.get_adjustment()
                adjustment.set_value(default_value)
                print(f"User set state: {state_type.name} with offset: {default_value}")
            except (IndexError, KeyError) as e:
                print(f"Error setting state: {e}")

    def on_advanced_settings_toggle(self, button, _pspec):
        """Handle toggling of advanced settings.

        When advanced settings are enabled:
        1. Show the advanced settings panels
        2. Disable the intended_state_combo to prevent conflicts

        When disabled, hide the panels and re-enable the combo.
        """
        if button.get_active():
            self.advanced_audio_settings.set_property("opacity", 1.0)

            # TODO:
            # self.advanced_visual_settings.set_property("opacity", 1.0)
            self.intended_state_combo.set_sensitive(False)

            # Block Signal being emitted since the offset is changing the intended_state_combo
            GObject.signal_handler_block(self.intended_state_combo, self.state_handler_id)

        else:
            self.advanced_audio_settings.set_property("opacity", 0)
            self.intended_state_combo.set_sensitive(True)

            # TODO
            # self.advanced_visual_settings.set_property("opacity", 0)

            # Unblock Signal being emitted since user is not using advanced settings
            GObject.signal_handler_unblock(self.intended_state_combo, self.state_handler_id)

    def _on_playing_state_changed(self, controller, _pspec):
        """Toggle minutes_spin_button sensitivity based on playback state."""
        is_playing = controller.is_playing
        self.minutes_spin_button.set_sensitive(not is_playing)

    def _get_state_name(self, offset_value):
        """Get the state name for the given offset."""
        for state, state_obj in STATE_DATA.items():
            if state_obj[LOWER_BOUND] <= offset_value <= state_obj[UPPER_BOUND]:
                return state.value
        return None

    def _on_channel_offset_changed(self, spin_row, _pspec):
        """Update when channel offset is changed."""
        offset_value = float(spin_row.get_value())
        state_index = self._get_state_name(offset_value)
        state_type = StateType(state_index)

        self.intended_state_combo.set_selected(state_index)
        self.intended_state_combo.set_title(
            f"{STATE_TYPE_NAMES[state_index]} ({STATE_DATA[state_type][DEFAULT]} Hz)"
        )

    def set_bindings(self):
        """Helper method for establishing bindings for the relevant widgets."""
        self.state_handler_id = self.intended_state_combo.connect(
            "notify::selected-item", self.on_intended_state_combo_changed
        )
        self.offset_handler_id = self.channel_offset_scale.connect(
            "notify::value", self._on_channel_offset_changed
        )

        self.advanced_settings_switch.connect("notify::active", self.on_advanced_settings_toggle)
        self.controller.connect("notify::is-playing", self._on_playing_state_changed)
