# visual_stimulus.py
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

"""Visual stimulus renderer for mental state induction."""

import math
from typing import Optional
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GObject, GLib
from .animations import get_animation_class
from .animations.base import Animation


class VisualStimulus(GObject.Object):
    """Visual stimulus renderer for mental state induction."""

    __gtype_name__ = "VisualStimulus"

    def __init__(self):
        super().__init__()
        self._enable_visual_stimuli = False
        self._stimuli_type = 0
        self._is_playing = False
        self._animation_source: Optional[int] = None
        self._widget = None
        self._last_ts: Optional[float] = None
        self._animation: Optional[Animation] = None

    @GObject.Property(type=bool, default=False)
    def enable_visual_stimuli(self):
        return self._enable_visual_stimuli

    def get_enable_visual_stimuli(self):
        return self.enable_visual_stimuli

    def set_enable_visual_stimuli(self, value):
        self.enable_visual_stimuli = value

    @enable_visual_stimuli.setter
    def enable_visual_stimuli(self, value):
        """Set whether visual stimuli are enabled."""
        self._enable_visual_stimuli = value

    @GObject.Property(type=int, default=0)
    def stimuli_type(self):
        return self._stimuli_type

    def get_stimuli_type(self):
        return self.stimuli_type

    def set_stimuli_type(self, value):
        self.stimuli_type = value

    @stimuli_type.setter
    def stimuli_type(self, value):
        """Set the type of visual stimuli to use."""
        self._stimuli_type = value
        if self._is_playing:
            self._animation = get_animation_class(str(self._stimuli_type))()

    def play(self):
        """Start rendering visual stimuli."""
        if self._enable_visual_stimuli and not self._is_playing:
            self._is_playing = True
            self._animation = get_animation_class(str(self._stimuli_type))()
            if self._widget:
                self._start_animation()

    def pause(self):
        """Pause rendering visual stimuli."""
        if self._is_playing:
            self._is_playing = False
            self._stop_animation()

    def stop(self):
        """Stop rendering visual stimuli."""
        self._is_playing = False
        self._stop_animation()
        # Reset widget appearance
        if self._widget:
            self._widget.queue_draw()

    def set_widget(self, widget):
        """Set the widget to render visual stimuli on."""
        self._widget = widget

    def _start_animation(self):
        """Start the animation loop."""
        if self._animation_source is None:
            self._last_ts = GLib.get_monotonic_time() / 1_000_000.0
            self._animation_source = GLib.timeout_add(16, self._animate)

    def _stop_animation(self):
        """Stop the animation loop."""
        if self._animation_source:
            GLib.source_remove(self._animation_source)
            self._animation_source = None

    def _animate(self):
        """Animation callback."""
        if self._is_playing and self._widget:
            now = GLib.get_monotonic_time() / 1_000_000.0
            dt = max(0.0, min(0.1, (now - (self._last_ts or now))))
            self._last_ts = now
            # Determine width/height for non-GTK test widgets
            if hasattr(self._widget, "get_allocation"):
                alloc = self._widget.get_allocation()
                width = getattr(alloc, "width", 0)
                height = getattr(alloc, "height", 0)
            else:
                width = getattr(self._widget, "width", 0)
                height = getattr(self._widget, "height", 0)
            if self._animation is not None:
                self._animation.update(dt, width, height)
            if hasattr(self._widget, "queue_draw"):
                self._widget.queue_draw()
            return GLib.SOURCE_CONTINUE
        return GLib.SOURCE_REMOVE

    def render(self, widget, cr, width, height):
        """Render the visual stimulus on the given cairo context."""
        if not self._enable_visual_stimuli:
            # Draw a simple background when not active
            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.rectangle(0, 0, width, height)
            cr.fill()
            return

        if not self._is_playing:
            # Draw a simple background when not playing
            cr.set_source_rgb(0.1, 0.1, 0.1)
            cr.rectangle(0, 0, width, height)
            cr.fill()
            return

        # Initialize animation if not already done (for backward compatibility with tests)
        if self._animation is None:
            self._animation = get_animation_class(str(self._stimuli_type))()

        # Use animation-driven state only
        self._animation.render(cr, width, height, 0.0)

    def _render_color_stimulus(self, cr, width, height, time):
        """Render a color-based stimulus."""
        # Calculate color based on time
        red = (math.sin(time * 2) + 1) / 2
        green = (math.sin(time * 3) + 1) / 2
        blue = (math.sin(time * 4) + 1) / 2

        # Set color and fill rectangle
        cr.set_source_rgb(red, green, blue)
        cr.rectangle(0, 0, width, height)
        cr.fill()

    def _render_breath_pattern_stimulus(self, cr, width, height, time):
        """Render a breath pattern stimulus."""
        # Calculate radius based on time (pulsing effect)
        max_radius = min(width, height) / 2
        radius = (math.sin(time * 2) + 1) / 2 * max_radius

        # Set color (blue-ish)
        cr.set_source_rgb(0.2, 0.4, 0.8)

        # Draw circle in center
        cr.arc(width / 2, height / 2, radius, 0, 2 * math.pi)
        cr.fill()
