# preferences_window.py
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

"""Preferences window for the Elevate application."""

from gi.repository import Adw, Gtk

from elevate.constants import (
    DESCRIPTION,
    LANGUAGES,
    StateType,
    STATE_DATA,
    STATE_TYPE_NAMES,
)

# pylint: disable=E1101,W0718


@Gtk.Template(resource_path="/org/thecodenomad/elevate/preferences_window.ui")
class PreferencesWindow(Adw.PreferencesDialog):
    """The Preferences Window exposing user selected defaults."""

    __gtype_name__ = "PreferencesWindow"

    # General Settings
    epileptic_warning_switch: Adw.SwitchRow = Gtk.Template.Child()
    language_selection_combo: Adw.ComboRow = Gtk.Template.Child()
    minutes_spin_button: Adw.SpinRow = Gtk.Template.Child()

    # Stimuli Settings
    default_state_combo: Adw.ComboRow = Gtk.Template.Child()
    default_visual_stimuli_combo: Adw.ComboRow = Gtk.Template.Child()
    breath_type: Adw.ComboRow = Gtk.Template.Child()

    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)

        self.settings = settings

        self._populate_combo_row(self.language_selection_combo, LANGUAGES)
        self._populate_combo_row(self.default_state_combo, STATE_TYPE_NAMES)

        self.set_bindings()
        self.set_default_states()

    def set_bindings(self):
        """Helper method to set the bindings for the Preferences window."""
        self.epileptic_warning_switch.connect("notify::active", self._on_epileptic_warning_toggle)
        self.language_selection_combo.connect("notify::selected", self._on_lang_changed)
        self.minutes_spin_button.connect("notify::value", self._on_session_length_changed)
        self.default_state_combo.connect("notify::selected", self._on_default_state_changed)

    def set_default_states(self):
        """Helper method to set the default states for the Preferences widgets."""

        # Set language
        idx = self.settings.language
        self.language_selection_combo.set_selected(idx)

        # Set intended state
        idx = self.settings.intended_state
        state_type = StateType(idx)
        self.default_state_combo.set_selected(idx)
        self.default_state_combo.set_tooltip_text(STATE_DATA[state_type][DESCRIPTION])

        # Set session length
        idx = self.settings.session_length
        self.minutes_spin_button.set_value(idx)

        # Set epileptic warning
        self.epileptic_warning_switch.set_active(self.settings.epileptic_warning)

    def _on_default_state_changed(self, combo, _pspec):
        sel = combo.get_selected()
        self.settings.intended_state = sel

        state_type = StateType(sel)
        self.default_state_combo.set_tooltip_text(STATE_DATA[state_type][DESCRIPTION])
        print(f"Saving default intended state to: {sel} - {STATE_TYPE_NAMES[sel]}")

    def _on_epileptic_warning_toggle(self, button, _pspec):
        print(f"Toggling epileptic warning to: {self.settings.epileptic_warning}")
        self.settings.epileptic_warning = button.get_active()

    def _on_lang_changed(self, *_):
        sel = self.language_selection_combo.get_selected()
        self.settings.language = sel

    def _on_session_length_changed(self, row, _pspec):
        session_length = row.get_value()
        self.settings.session_length = session_length

    def _populate_combo_row(self, combo_row, entries):
        string_list = Gtk.StringList.new(entries)
        combo_row.set_model(string_list)
