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

    frequency_scale = Gtk.Template.Child()
    channel_offset_scale = Gtk.Template.Child()
    visual_stimuli_switch = Gtk.Template.Child()
    stimuli_type_combo = Gtk.Template.Child()

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.stimuli_type_combo.connect('notify::selected-item', self._on_stimuli_type_combo_changed)

    def _on_stimuli_type_combo_changed(self, combo, pspec):
        selected_item = combo.get_selected_item().get_string()
        if selected_item == "Bounce":
            self.controller.set_stimuli_type(0)