# epileptic_warning_dialog.py
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

"""Epileptic warning dialog for the Elevate application."""

from gi.repository import Adw, Gtk


# pylint: disable=W0246,R0903


@Gtk.Template(resource_path="/org/thecodenomad/elevate/epileptic_warning_dialog.ui")
class EpilepticWarningDialog(Adw.AlertDialog):
    """Dialog shown for user to acknowledge the epileptic warning."""

    __gtype_name__ = "EpilepticWarningDialog"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
