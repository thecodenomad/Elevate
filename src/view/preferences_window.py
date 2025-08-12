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

from gi.repository import Adw, Gio, Gtk

from elevate.constants import LANGUAGES, LANGUAGE_CODES, StateType, RANGES, STATE_TYPE_NAMES


@Gtk.Template(resource_path="/org/thecodenomad/elevate/preferences_window.ui")
class PreferencesWindow(Adw.PreferencesDialog):
    __gtype_name__ = "PreferencesWindow"

    # General Settings
    show_epileptic_warning: Adw.SwitchRow = Gtk.Template.Child()
    language_selection_combo: Adw.ComboRow = Gtk.Template.Child()
    minutes_spin_button: Adw.SpinRow = Gtk.Template.Child()

    # Stimuli Settings
    default_state_combo: Adw.ComboRow = Gtk.Template.Child()
    default_visual_stimuli_combo: Adw.ComboRow = Gtk.Template.Child()
    breath_type: Adw.ComboRow = Gtk.Template.Child()

    def __init__(self, settings, **kwargs):
        super().__init__(**kwargs)

        self._settings = settings

        self._populate_combo_row(self.language_selection_combo, LANGUAGES)
        self._populate_combo_row(self.default_state_combo, STATE_TYPE_NAMES)

        self.set_bindings()
        self.set_default_states()

    def set_bindings(self):
        """Helper method to set the bindings for the Preferences window."""
        self.language_selection_combo.connect("notify::selected", self._on_lang_changed)
        self.minutes_spin_button.connect("notify::value", self._on_session_length_changed)
        self.default_state_combo.connect("notify::selected", self._on_default_state_changed)


    def set_default_states(self):
        """Helper method to set the default states for the Preferences widgets."""
        # Set Default Language
        try:
            current = self._settings.get_string("language")
            idx = LANGUAGE_CODES.index(current) if current in LANGUAGE_CODES else 0
        except Exception:
            idx = 0
        self.language_selection_combo.set_selected(idx)

        # Set Default State
        try:
            state_idx = self._settings.get_int("default-state")
        except Exception:
            state_idx = 0
        self.default_state_combo.set_selected(state_idx)

        # Set Default Session Length
        try:
            session_length = self._settings.get_int("default-session-length")
        except Exception:
            session_length = 10
        self.minutes_spin_button.set_value(session_length)

    def _on_default_state_changed(self, combo, pspec):
        sel = combo.get_selected()
        self._settings.set_int("default-state", sel)
        print(f"Saving default intended state to: {sel} - {STATE_TYPE_NAMES[sel]}")

    def _on_lang_changed(self, *_):
        sel = self.language_selection_combo.get_selected()
        if 0 <= sel < len(LANGUAGES):
            self._settings.set_string("language", LANGUAGE_CODES[sel])

    def _on_session_length_changed(self, row, pspec):
        session_length = row.get_value()
        self._settings.set_int("default-session-length", session_length)

    def _populate_combo_row(self, combo_row, entries):
        string_list = Gtk.StringList.new(entries)
        combo_row.set_model(string_list)
