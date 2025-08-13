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

"""Visual stimulus renderer for mental state induction.

This module provides the VisualStimulus class which handles rendering of
visual stimuli for mental state induction. It supports various animation
types and manages the animation loop using GLib timers.
"""

import math
from typing import Optional
import gi

gi.require_version("Gtk", "4.0")
from gi.repository import GObject, GLib
from .animations import get_animation_class
from .animations.base import Animation

# pylint: disable=R0902


class VisualStimulus(GObject.Object):
    """Visual stimulus renderer for mental state induction.

    This class manages the rendering of visual stimuli using various
    animation types. It handles the animation loop, timing, and rendering
    of visual effects using Cairo graphics.

    Attributes:
        enable_visual_stimuli (bool): Whether visual stimuli are enabled.
        stimuli_type (int): Type of visual stimuli to use.
    """

    __gtype_name__ = "VisualStimulus"

    def __init__(self):
        """Initialize the VisualStimulus instance."""
        super().__init__()
        self._enable_visual_stimuli = False
        self._stimuli_type = 0
        self._is_playing = False
        self._animation_source: Optional[int] = None
        self._widget = None
        self._last_ts: Optional[float] = None
        self._animation: Optional[Animation] = None
        self._time = 0.0  # Accumulated time for animations

    @GObject.Property(type=bool, default=False)
    def enable_visual_stimuli(self):
        """Get whether visual stimuli are enabled.

        Returns:
            bool: True if visual stimuli are enabled, False otherwise.
        """
        return self._enable_visual_stimuli

    @enable_visual_stimuli.setter
    def enable_visual_stimuli(self, value):
        """Set whether visual stimuli are enabled.

        Args:
            value (bool): True to enable visual stimuli, False to disable.
        """
        self._enable_visual_stimuli = value

    @GObject.Property(type=int, default=0)
    def stimuli_type(self):
        """Get the type of visual stimuli to use.

        Returns:
            int: The type of visual stimuli.
        """
        return self._stimuli_type

    @stimuli_type.setter
    def stimuli_type(self, value):
        """Set the type of visual stimuli to use.

        Args:
            value (int): The type of visual stimuli to use.
        """
        self._stimuli_type = value
        if self._is_playing:
            self._animation = get_animation_class(str(self._stimuli_type))()

    def play(self):
        """Start rendering visual stimuli.

        Initializes the animation and starts the animation loop if
        visual stimuli are enabled and not already playing.
        """
        if self._enable_visual_stimuli and not self._is_playing:
            self._is_playing = True
            self._animation = get_animation_class(str(self._stimuli_type))()
            if self._widget:
                self._start_animation()

    def pause(self):
        """Pause rendering visual stimuli.

        Stops the animation loop and resets the accumulated time.
        """
        if self._is_playing:
            self._is_playing = False
            self._time = 0.0  # Reset time on pause
            self._stop_animation()

    def stop(self):
        """Stop rendering visual stimuli.

        Stops the animation loop, resets the accumulated time, and
        triggers a redraw of the widget.
        """
        self._is_playing = False
        self._time = 0.0  # Reset time on stop
        self._stop_animation()
        # Reset widget appearance
        if self._widget:
            self._widget.queue_draw()

    def set_widget(self, widget):
        """Set the widget to render visual stimuli on.

        Args:
            widget: The GTK widget to render on.
        """
        self._widget = widget

    # pylint: disable=E1120
    def _start_animation(self):
        """Start the animation loop.

        Initializes the animation timer and starts calling the animation
        callback at regular intervals.
        """

        if self._animation_source is None:
            print("Animation should be starting...")
            self._last_ts = GLib.get_monotonic_time() / 1_000_000.0
            self._animation_source = GLib.timeout_add(16, self._animate)

    # pylint: enable=E1101

    def _stop_animation(self):
        """Stop the animation loop.

        Removes the animation timer and cleans up the animation source.
        """
        if self._animation_source:
            GLib.source_remove(self._animation_source)
            self._animation_source = None

    # pylint: disable=E1120
    def _animate(self):
        """Animation callback.

        Called periodically to update the animation state and trigger
        widget redraws.

        Returns:
            bool: GLib.SOURCE_CONTINUE to continue the animation loop.
        """
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
                self._time += dt  # Accumulate time
            if hasattr(self._widget, "queue_draw"):
                self._widget.queue_draw()
            return GLib.SOURCE_CONTINUE
        return GLib.SOURCE_REMOVE

    # pylint: enable=E1120

    def render(self, _widget, cr, width, height):
        """Render the visual stimulus on the given cairo context.

        Args:
            widget: The GTK widget being rendered.
            cr: The Cairo context to draw on.
            width (int): The width of the drawing area.
            height (int): The height of the drawing area.
        """
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

        # Use animation-driven state with accumulated time
        self._animation.render(cr, width, height, self._time)

    def _render_color_stimulus(self, cr, width, height, time):
        """Render a color-based stimulus.

        Args:
            cr: The Cairo context to draw on.
            width (int): The width of the drawing area.
            height (int): The height of the drawing area.
            time (float): The current time for animation calculations.
        """
        # Calculate color based on time
        red = (math.sin(time * 2) + 1) / 2
        green = (math.sin(time * 3) + 1) / 2
        blue = (math.sin(time * 4) + 1) / 2

        # Set color and fill rectangle
        cr.set_source_rgb(red, green, blue)
        cr.rectangle(0, 0, width, height)
        cr.fill()

    def _render_breath_pattern_stimulus(self, cr, width, height, time):
        """Render a breath pattern stimulus.

        Args:
            cr: The Cairo context to draw on.
            width (int): The width of the drawing area.
            height (int): The height of the drawing area.
            time (float): The current time for animation calculations.
        """
        # Calculate radius based on time (pulsing effect)
        max_radius = min(width, height) / 2
        radius = (math.sin(time * 2) + 1) / 2 * max_radius

        # Set color (blue-ish)
        cr.set_source_rgb(0.2, 0.4, 0.8)

        # Draw circle in center
        cr.arc(width / 2, height / 2, radius, 0, 2 * math.pi)
        cr.fill()
