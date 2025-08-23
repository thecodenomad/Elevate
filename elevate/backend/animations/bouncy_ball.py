"""Bouncy ball animation implementation.

This module provides the BouncyBallAnimation class which implements
a breathing-focused animation with a bouncing ball effect. The animation
cycles through four phases that represent breathing patterns:
inhale, hold, exhale, and hold.

The animation can be customized with different colors, durations,
and visual cues to support guided breathing exercises.
"""

from __future__ import annotations

import math
from typing import Tuple, Optional

from elevate.backend.animations.base import Animation, CairoContext
from elevate.constants import StateType

# Default color constants
SOFT_BLUE = (0.2, 0.6, 0.9)  # Color for breath phases
LAVENDER = (0.6, 0.4, 0.8)  # Color for hold phases
DEEP_INDIGO = (0.2, 0.2, 0.6)  # Background color

# Brain wave state color schemes
BRAIN_WAVE_COLORS = {
    StateType.DELTA: {
        "breath": (0.1, 0.1, 0.4),  # Deep navy for calming immersion
        "hold": (0.2, 0.0, 0.3),  # Dark purple for profound stillness
        "background": (0.05, 0.05, 0.2),  # Midnight indigo for ultimate depth
    },
    StateType.THETA: {
        "breath": (0.2, 0.6, 0.9),  # Color for breath phases
        "hold": (0.6, 0.4, 0.8),  # Color for hold phases
        "background": (0.2, 0.2, 0.6),  # Background color
    },
    StateType.ALPHA: {
        "breath": (0.4, 0.8, 0.5),  # Soft green for gentle harmony
        "hold": (0.6, 0.8, 0.2),  # Light lime for subtle uplift
        "background": (0.2, 0.5, 0.3),  # Muted forest green for grounded calm
    },
    StateType.BETA: {
        "breath": (0.9, 0.3, 0.2),  # Warm orange for energizing flow
        "hold": (0.8, 0.5, 0.1),  # Amber for sustained attention
        "background": (0.6, 0.2, 0.1),  # Deep terracotta for motivational grounding
    },
    StateType.GAMMA: {
        "breath": (0.9, 0.8, 0.2),  # Bright yellow for clarity and insight
        "hold": (0.9, 0.7, 0.0),  # Golden for heightened awareness
        "background": (0.7, 0.6, 0.1),  # Warm mustard for cognitive stimulation
    },
}

# For a complete implementation, we would use Cairo text rendering functions:
# Define constants for font slant and weight (these would normally come from cairo)
FONT_SLANT_NORMAL = 0
FONT_WEIGHT_BOLD = 1


class BouncyBallAnimation(Animation):
    """Bouncy ball animation implementation for breathing guidance.

    This animation creates a visual breathing guide using a pulsating
    circle that represents a bouncing ball. The animation consists of
    four distinct phases:

    1. Inhale: Circle grows from small to large
    2. Hold: Circle pulses gently at maximum size
    3. Exhale: Circle shrinks from large to small
    4. Hold: Circle pulses gently at minimum size

    The animation supports color transitions, customizable durations,
    and visual/audio cues for each phase.
    """

    def __init__(
        self,
        breath_color: tuple[float, float, float] = BRAIN_WAVE_COLORS[StateType.THETA]["breath"],
        hold_color: tuple[float, float, float] = BRAIN_WAVE_COLORS[StateType.THETA]["hold"],
        background: tuple[float, float, float] = BRAIN_WAVE_COLORS[StateType.THETA]["background"],
        pulse_factor: float = 0.05,
        fade_duration: float = 0.5,
        brain_wave_state: Optional[str] = None,
    ) -> None:
        """Initialize the BouncyBall animation with configurable parameters.

        Args:
            breath_color: RGB color tuple for inhale/exhale phases (0.0 to 1.0 range)
            hold_color: RGB color tuple for hold phases (0.0 to 1.0 range)
            background: RGB color tuple for background (0.0 to 1.0 range)
            pulse_factor: Intensity of pulsation effect during hold phases (0.0 to 1.0)
            fade_duration: Duration for color fading transitions in seconds
            brain_wave_state: Optional brain wave state to use predefined color scheme

        Attributes:
            breath_color (tuple[float, float, float]): Color for breath phases
            hold_color (tuple[float, float, float]): Color for hold phases
            background (tuple[float, float, float]): Background color
            pulse_factor (float): Pulsation intensity factor
            fade_duration (float): Color transition duration
            phase_cues (list[str]): Phase cue texts for visual guidance
            brain_wave_state (str): Current brain wave state for color scheme
        """
        # Set colors based on brain wave state if provided
        if brain_wave_state and brain_wave_state.lower() in BRAIN_WAVE_COLORS:
            colors = BRAIN_WAVE_COLORS[brain_wave_state.lower()]
            self.breath_color = colors["breath"]
            self.hold_color = colors["hold"]
            self.background = colors["background"]
            self.brain_wave_state = brain_wave_state.lower()
        else:
            self.breath_color = breath_color
            self.hold_color = hold_color
            self.background = background
            self.brain_wave_state = brain_wave_state

        self.pulse_factor = pulse_factor
        self.fade_duration = fade_duration
        self.phase_durations = (4.0, 4.0, 4.0, 4.0)  # Default phase durations
        self.phase_cues = ["Inhale", "Hold", "Exhale", "Hold"]  # Visual/audio cues for each phase
        self._t = 0.0

        # Cache calculated values for performance
        self._phase_ends = None
        self._total_cycle = None
        self._fade_half = None
        self._last_width = None
        self._last_height = None
        self._last_max_radius = None
        self._last_phase = None
        self._last_cue_text = None

    def _update_cached_values(self) -> None:
        """Update cached calculation values for performance optimization."""
        if self._total_cycle is None:
            # Calculate total cycle duration
            self._total_cycle = sum(self.phase_durations)

            # Calculate fade half duration
            self._fade_half = self.fade_duration / 2.0

            # Calculate phase boundaries only when needed
            self._phase_ends = [0.0]
            for duration in self.phase_durations:
                self._phase_ends.append(self._phase_ends[-1] + duration)

    def reset(self) -> None:
        """Reset the animation to its initial state.

        Sets the animation time counter back to zero, effectively
        restarting the breathing cycle from the beginning.
        """
        self._t = 0.0
        self._last_phase = None  # Reset phase cache

    def set_breath_cycle(self, cycle: Tuple[float, float, float, float]) -> None:
        """Set the duration of each phase (inhale, hold1, exhale, hold2).

        Args:
            cycle: Tuple of durations for each phase in seconds as
                (inhale_duration, hold1_duration, exhale_duration, hold2_duration)
        """
        self.phase_durations = cycle

    def set_brain_wave_state(self, state: str) -> None:
        """Set the brain wave state and update colors accordingly.

        Args:
            state: Brain wave state (delta, alpha, beta, gamma)
        """
        state_lower = state.lower()
        if state_lower in BRAIN_WAVE_COLORS:
            colors = BRAIN_WAVE_COLORS[state_lower]
            self.breath_color = colors["breath"]
            self.hold_color = colors["hold"]
            self.background = colors["background"]
            self.brain_wave_state = state_lower
            # Reset cached values to force recalculation with new colors
            self._total_cycle = None

    def set_phase_cues(
        self, cues: Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]
    ) -> None:
        """Set the phase cues for each of the 4 phases.

        Args:
            cues: Tuple of cues for each phase (phase1, phase2, phase3, phase4)
                  Each cue can be None (disabled), text (visual cue), or path to audio file
        """
        self.phase_cues = list(cues)

    def is_phase_active(self, phase_index: int, t: float) -> bool:
        """Check if a specific phase is active at time t.

        Args:
            phase_index: Index of phase (0-3)
            t: Time in seconds

        Returns:
            bool: True if phase is active, False otherwise
        """
        if sum(self.phase_durations) == 0:
            return False
        phase_start = sum(self.phase_durations[:phase_index])
        phase_end = phase_start + self.phase_durations[phase_index]
        return phase_start <= t % sum(self.phase_durations) < phase_end

    def update(self, dt: float, width: int, height: int) -> None:
        """Update the animation state based on elapsed time.

        Advances the internal time counter by the specified delta time.
        This method is called periodically to update the animation's
        internal state.

        Args:
            dt: Time elapsed since last update in seconds
            width: Current width of the drawing area (unused)
            height: Current height of the drawing area (unused)
        """
        self._t += dt

    def phase1(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 1: Inhale - Growing from 0 to max_radius.

        The circle grows from its minimum size to the maximum size
        over the duration of the inhale phase.

        Args:
            t: Time within the current phase in seconds
            max_radius: Maximum radius of the circle

        Returns:
            tuple[float, tuple[float, float, float]]: Current radius and color as (radius, color)
        """
        duration = self.phase_durations[0]
        if duration == 0:
            return 0.0, self.breath_color
        radius = (t / duration) * max_radius * (1.0 - self.pulse_factor)
        return radius, self.breath_color

    def phase2(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 2: Hold - Pulsating between max_radius * (1 - pulse_factor) and max_radius.

        The circle gently pulses at its maximum size during the hold phase.

        Args:
            t: Time within the current phase in seconds
            max_radius: Maximum radius of the circle

        Returns:
            tuple[float, tuple[float, float, float]]: Current radius and color as (radius, color)
        """
        pulse_time = t - self.phase_durations[0]
        # Period of 1 second for pulsation
        pulse = 0.5 * (1.0 + math.cos(2.0 * math.pi * pulse_time / 1.0 + math.pi))
        min_radius = max_radius * (1.0 - self.pulse_factor)
        radius = min_radius + (max_radius - min_radius) * pulse
        return radius, self.hold_color

    def phase3(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 3: Exhale - Shrinking from max_radius to 0.

        The circle shrinks from its maximum size to minimum size
        over the duration of the exhale phase.

        Args:
            t: Time within the current phase in seconds
            max_radius: Maximum radius of the circle

        Returns:
            tuple[float, tuple[float, float, float]]: Current radius and color as (radius, color)
        """
        phase_start = sum(self.phase_durations[:2])
        duration = self.phase_durations[2]
        if duration == 0:
            return 0.0, self.breath_color
        radius = (1.0 - ((t - phase_start) / duration)) * max_radius * (1.0 - self.pulse_factor)
        return radius, self.breath_color

    def phase4(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 4: Hold - Pulsating between 0 and max_radius * pulse_factor.

        The circle gently pulses at its minimum size during the hold phase.

        Args:
            t: Time within the current phase in seconds
            max_radius: Maximum radius of the circle

        Returns:
            tuple[float, tuple[float, float, float]]: Current radius and color as (radius, color)
        """
        phase_start = sum(self.phase_durations[:3])
        pulse_time = t - phase_start
        # Period of 1 second for pulsation
        pulse = 0.5 * (1.0 + math.cos(2.0 * math.pi * pulse_time / 1.0 + math.pi))
        radius = max_radius * self.pulse_factor * pulse
        return radius, self.hold_color

    def interpolate_color(
        self, color1: tuple[float, float, float], color2: tuple[float, float, float], alpha: float
    ) -> tuple[float, float, float]:
        """Interpolate between two RGB colors based on alpha (0 to 1).

        Args:
            color1: First RGB color tuple (r, g, b)
            color2: Second RGB color tuple (r, g, b)
            alpha: Interpolation factor (0.0 = color1, 1.0 = color2)

        Returns:
            tuple[float, float, float]: Interpolated RGB color tuple
        """
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return (r1 + (r2 - r1) * alpha, g1 + (g2 - g1) * alpha, b1 + (b2 - b1) * alpha)

    def render(self, cr: CairoContext, width: int, height: int, now_s: float) -> None:
        """Render the animation with phase-specific logic and color fading.

        Draws the current frame of the animation, including the bouncing
        ball circle and any active phase cues. Handles all phase transitions,
        color fading, and visual effects.

        Args:
            cr: Cairo context for drawing operations
            width: Width of the drawing area
            height: Height of the drawing area
            now_s: Current time in seconds for animation calculations
        """
        # Update cached values if needed
        self._update_cached_values()

        if self._total_cycle == 0:
            # Handle edge case of zero total duration
            cr.set_source_rgb(*self.background)
            if hasattr(cr, "paint"):
                cr.paint()
            return

        t = self._t % self._total_cycle

        # Cache max_radius calculation
        if self._last_width != width or self._last_height != height:
            self._last_width = width
            self._last_height = height
            self._last_max_radius = min(width, height) / 2
        max_radius = self._last_max_radius

        # Set background color
        cr.set_source_rgb(*self.background)
        if hasattr(cr, "paint"):
            cr.paint()

        # Determine phase boundaries
        phase_ends = [0.0]
        for duration in self.phase_durations:
            phase_ends.append(self._phase_ends[-1] + duration)

        # Calculate radius and base color based on current phase
        if t <= self._phase_ends[1]:  # Phase 1: Inhale
            radius, base_color = self.phase1(t, max_radius)
        elif t <= self._phase_ends[2]:  # Phase 2: Hold
            radius, base_color = self.phase2(t, max_radius)
        elif t <= self._phase_ends[3]:  # Phase 3: Exhale
            radius, base_color = self.phase3(t, max_radius)
        else:  # Phase 4: Hold
            radius, base_color = self.phase4(t, max_radius)

        # Handle color fading at phase transitions
        color = base_color
        for i, end in enumerate(self._phase_ends[1:], 1):
            if end - self._fade_half < t < end + self._fade_half:
                alpha = (t - (end - self._fade_half)) / self.fade_duration
                prev_color = self.breath_color if i % 2 == 1 else self.hold_color
                next_color = self.hold_color if i % 2 == 1 else self.breath_color
                color = self.interpolate_color(prev_color, next_color, alpha)
                break
        if t < self._fade_half:  # Handle loop from end to beginning
            alpha = (t + self._fade_half) / self.fade_duration
            color = self.interpolate_color(self.hold_color, self.breath_color, alpha)

        # Render the circle
        cr.set_source_rgb(*color)
        cr.arc(width / 2, height / 2, radius, 0, 2 * math.pi)
        if hasattr(cr, "fill"):
            cr.fill()

        # Render phase cue if active (only when phase changes)
        current_phase = 0
        for i, end in enumerate(self._phase_ends[1:]):
            if t <= end:
                current_phase = i
                break

        # Check if cue is enabled for current phase and phase has changed
        if self.phase_cues[current_phase] is not None and self._last_phase != current_phase:
            self._last_phase = current_phase
            self._last_cue_text = self.phase_cues[current_phase]
            self._render_phase_cue(cr, current_phase, width, height)
        elif (
            self.phase_cues[current_phase] is not None
            and self._last_phase == current_phase
            and self._last_cue_text == self.phase_cues[current_phase]
        ):
            # Phase hasn't changed, render the same cue again
            self._render_phase_cue(cr, current_phase, width, height)

    def _render_phase_cue(self, cr: CairoContext, phase_index: int, _width: int, height: int) -> None:
        """Render a visual phase cue.

        Args:
            cr: Cairo context
            phase_index: Index of the current phase (0-3)
            _width: Width of the rendering area
            height: Height of the rendering area
        """
        # Phase cue text mapping
        cue_text = {
            0: "Inhale",  # Phase 1
            1: "Hold",  # Phase 2
            2: "Exhale",  # Phase 3
            3: "Hold",  # Phase 4
        }

        # Skip if text cue not properly set
        if self.phase_cues[phase_index] != cue_text[phase_index]:
            return

        # Set up text rendering
        cr.set_source_rgb(1.0, 1.0, 1.0)  # White text

        cr.select_font_face("Sans", FONT_SLANT_NORMAL, FONT_WEIGHT_BOLD)
        cr.set_font_size(48)

        # Ensure we have a valid text cue
        cue_text = self.phase_cues[phase_index]
        if cue_text is None:
            return

        cr.text_extents(cue_text)
        x = 12  # width / 2 - text_width / 2
        y = height - 20  # height / 2 - text_height / 2 + 20
        cr.move_to(x, y)
        cr.show_text(cue_text)
