# stimuli_renderer.py
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

"""Stimuli renderer widget for the Elevate application."""

from gi.repository import Gtk


@Gtk.Template(resource_path="/org/thecodenomad/elevate/stimuli_renderer.ui")
class StimuliRenderer(Gtk.DrawingArea):
    """Handles the main stimuli visual content."""

    __gtype_name__ = "StimuliRenderer"

    def __init__(self, controller=None, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller

        # Connect to draw signal
        self.set_draw_func(self._on_draw)

        # If controller is provided, connect to visual stimulus
        if self.controller and hasattr(self.controller, "visual_stimulus"):
            self.controller.visual_stimulus.set_widget(self)

    def _on_draw(self, _area, cr, width, height):
        """Handle draw signal."""
        # If we have a controller with visual stimulus, delegate rendering
        if self.controller and hasattr(self.controller, "visual_stimulus"):
            self.controller.visual_stimulus.render(self, cr, width, height)
        else:
            # Draw a simple background if no controller
            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.rectangle(0, 0, width, height)
            cr.fill()
