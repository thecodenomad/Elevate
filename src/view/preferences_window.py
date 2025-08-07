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


@Gtk.Template(resource_path='/org/thecodenomad/elevate/preferences_window.ui')
class PreferencesWindow(Adw.PreferencesDialog):
    __gtype_name__ = 'PreferencesWindow'

    show_epileptic_warning = Gtk.Template.Child()
    language_selection = Gtk.Template.Child()
    default_state = Gtk.Template.Child()
    default_visual_stimuli = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
