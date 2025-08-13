# control_sidebar.py
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
from gi.repository import Gtk

# Import constants using relative import
from elevate.constants import DEFAULT, STATE_DATA, StateType


@Gtk.Template(resource_path="/org/thecodenomad/elevate/sidebar.ui")
class Sidebar(Gtk.Box):
    """Control sidebar for the Elevate application."""

    __gtype_name__ = "Sidebar"

    intended_state_combo = Gtk.Template.Child()
    minutes_spin_button = Gtk.Template.Child()
    advanced_settings_switch = Gtk.Template.Child()

    advanced_audio_settings = Gtk.Template.Child()
    advanced_visual_settings = Gtk.Template.Child()

    frequency_scale = Gtk.Template.Child()
    channel_offset_scale = Gtk.Template.Child()
    visual_stimuli_switch = Gtk.Template.Child()
    stimuli_type_combo = Gtk.Template.Child()

    def __init__(self, controller, settings, **kwargs):
        """Initialize the sidebar."""
        super().__init__(**kwargs)
        self.controller = controller
        self.settings = settings
        self.set_bindings()
        self.set_defaults()

    def set_defaults(self):
        # Set Intended State
        state_idx = self.settings.intended_state
        self.intended_state_combo.set_selected(state_idx)

        # Set Default Session Length
        session_length = self.settings.session_length
        self.minutes_spin_button.set_value(session_length)

        # Set Default Base Frequency
        base_frequency = self.settings.base_frequency
        self.frequency_scale.set_value(base_frequency)

        # Set Enable Visual Stimuli
        enable_visuals = self.settings.enable_visual_stimuli
        self.visual_stimuli_switch.set_active(enable_visuals)

    def on_intended_state_combo_changed(self, combo, _pspec):
        """Handle changes to the intended_state_combo.

        When a user selects a state from the combo box, this method will:
        1. Map the selection to a StateType enum
        2. Set the channel_offset_scale to the default value for that state
        """
        selected_index = combo.get_selected()
        if selected_index != Gtk.INVALID_LIST_POSITION:
            # Map the index to the StateType enum
            try:
                state_type = list(StateType)[selected_index]
                # Set the channel_offset_scale to the default value for this state
                default_value = STATE_DATA[state_type][DEFAULT]
                adjustment = self.channel_offset_scale.get_adjustment()
                adjustment.set_value(default_value)
                print(f"User intends to state: {state_type.name}")
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
            self.advanced_visual_settings.set_property("opacity", 1.0)
            self.intended_state_combo.set_sensitive(False)
        else:
            self.advanced_audio_settings.set_property("opacity", 0)
            self.advanced_visual_settings.set_property("opacity", 0)
            self.intended_state_combo.set_sensitive(True)

    def on_stimuli_type_combo_changed(self, combo, _pspec):
        """Handle changes to the stimuli_type_combo.

        Currently only handles the "Bounce" selection which maps to stimuli type 0.
        """
        selected_item = combo.get_selected_item()
        if selected_item is not None:
            selected_string = selected_item.get_string()
            if selected_string == "Bounce":
                self.controller.set_stimuli_type(0)

    def set_bindings(self):
        self.intended_state_combo.connect("notify::selected-item", self.on_intended_state_combo_changed)
        self.stimuli_type_combo.connect("notify::selected-item", self.on_stimuli_type_combo_changed)
        self.advanced_settings_switch.connect("notify::active", self.on_advanced_settings_toggle)
