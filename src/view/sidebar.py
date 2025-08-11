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

from gi.repository import Gtk


@Gtk.Template(resource_path='/org/thecodenomad/elevate/sidebar.ui')
class Sidebar(Gtk.Box):
    __gtype_name__ = 'Sidebar'

    intended_state_combo = Gtk.Template.Child()
    minutes_spin_button = Gtk.Template.Child()
    advanced_settings_switch = Gtk.Template.Child()

    advanced_audio_settings = Gtk.Template.Child()
    advanced_visual_settings = Gtk.Template.Child()

    frequency_scale = Gtk.Template.Child()
    channel_offset_scale = Gtk.Template.Child()
    visual_stimuli_switch = Gtk.Template.Child()
    stimuli_type_combo = Gtk.Template.Child()

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.set_bindings()

    def _on_intended_state_combo_changed(self, combo, pspec):
        selected_item = combo.get_selected_item().get_string()
        print(f"User intends to state: {selected_item}")

    def _on_advanced_settings_toggle(self, button, pspec):
        if button.get_active():
            self.advanced_audio_settings.set_opacity(1.0)
            self.advanced_visual_settings.set_opacity(1.0)
            self.intended_state_combo.set_sensitive(False)
        else:
            self.advanced_audio_settings.set_opacity(0)
            self.advanced_visual_settings.set_opacity(0)
            self.intended_state_combo.set_sensitive(True)

    def _on_stimuli_type_combo_changed(self, combo, pspec):
        selected_item = combo.get_selected_item().get_string()
        if selected_item == "Bounce":
            self.controller.set_stimuli_type(0)

    def set_bindings(self):
        self.intended_state_combo.connect("notify::selected-item", self._on_intended_state_combo_changed)
        self.stimuli_type_combo.connect('notify::selected-item', self._on_stimuli_type_combo_changed)
        self.advanced_settings_switch.connect("notify::active", self._on_advanced_settings_toggle)
