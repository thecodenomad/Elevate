from __future__ import annotations

import math
from typing import Tuple, Optional

from .base import Animation, CairoContext

# Default color constants
SOFT_BLUE = (0.2, 0.6, 0.9)  # Color for breath phases
LAVENDER = (0.6, 0.4, 0.8)    # Color for hold phases
DEEP_INDIGO = (0.2, 0.2, 0.6)  # Background color

class BouncyBallAnimation(Animation):
    def __init__(self, breath_color: tuple[float, float, float] = SOFT_BLUE,
                 hold_color: tuple[float, float, float] = LAVENDER,
                 background: tuple[float, float, float] = DEEP_INDIGO,
                 pulse_factor: float = 0.05, fade_duration: float = 0.5) -> None:
        """
        Initialize the BouncyBall animation with configurable parameters.

        Args:
            breath_color: Color for inhale/exhale phases
            hold_color: Color for hold phases
            background: Background color
            pulse_factor: Intensity of pulsation effect (0.0 to 1.0)
            fade_duration: Duration for color fading transitions in seconds
        """
        self.breath_color = breath_color
        self.hold_color = hold_color
        self.background = background
        self._t = 0.0
        self.phase_durations = (4.0, 4.0, 4.0, 4.0)  # Default phase durations
        self.pulse_factor = pulse_factor
        self.fade_duration = fade_duration
        self.phase_cues = ["Inhale", "Hold", "Exhale", "Hold"]  # Visual/audio cues for each phase

    def reset(self) -> None:
        """Reset the animation to its initial state."""
        self._t = 0.0

    def set_breath_cycle(self, cycle: Tuple[float, float, float, float]) -> None:
        """Set the duration of each phase (inhale, hold1, exhale, hold2)."""
        self.phase_durations = cycle

    def set_phase_cues(self, cues: Tuple[Optional[str], Optional[str], Optional[str], Optional[str]]) -> None:
        """
        Set the phase cues for each of the 4 phases.

        Args:
            cues: Tuple of cues for each phase (phase1, phase2, phase3, phase4)
                  Each cue can be None (disabled), text (visual cue), or path to audio file
        """
        self.phase_cues = list(cues)

    def is_phase_active(self, phase_index: int, t: float) -> bool:
        """
        Check if a specific phase is active at time t.

        Args:
            phase_index: Index of phase (0-3)
            t: Time in seconds

        Returns:
            True if phase is active, False otherwise
        """
        if sum(self.phase_durations) == 0:
            return False
        phase_start = sum(self.phase_durations[:phase_index])
        phase_end = phase_start + self.phase_durations[phase_index]
        return phase_start <= t % sum(self.phase_durations) < phase_end

    def update(self, dt: float, width: int, height: int) -> None:
        """Update the animation state based on elapsed time."""
        self._t += dt

    def phase1(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 1: Inhale - Growing from 0 to max_radius."""
        duration = self.phase_durations[0]
        if duration == 0:
            return 0.0, self.breath_color
        radius = (t / duration) * max_radius * (1.0 - self.pulse_factor)
        return radius, self.breath_color

    def phase2(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 2: Hold - Pulsating between max_radius * (1 - pulse_factor) and max_radius."""
        pulse_time = t - self.phase_durations[0]
        # Period of 1 second for pulsation
        pulse = 0.5 * (1.0 + math.cos(2.0 * math.pi * pulse_time / 1.0 + math.pi))
        min_radius = max_radius * (1.0 - self.pulse_factor)
        radius = min_radius + (max_radius - min_radius) * pulse
        return radius, self.hold_color

    def phase3(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 3: Exhale - Shrinking from max_radius to 0."""
        phase_start = sum(self.phase_durations[:2])
        duration = self.phase_durations[2]
        if duration == 0:
            return 0.0, self.breath_color
        radius = (1.0 - ((t - phase_start) / duration)) * max_radius * (1.0 - self.pulse_factor)
        return radius, self.breath_color

    def phase4(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 4: Hold - Pulsating between 0 and max_radius * pulse_factor."""
        phase_start = sum(self.phase_durations[:3])
        pulse_time = t - phase_start
        # Period of 1 second for pulsation
        pulse = 0.5 * (1.0 + math.cos(2.0 * math.pi * pulse_time / 1.0 + math.pi))
        radius = max_radius * self.pulse_factor * pulse
        return radius, self.hold_color

    def interpolate_color(self, color1: tuple[float, float, float], color2: tuple[float, float, float], alpha: float) -> tuple[float, float, float]:
        """Interpolate between two RGB colors based on alpha (0 to 1)."""
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        return (
            r1 + (r2 - r1) * alpha,
            g1 + (g2 - g1) * alpha,
            b1 + (b2 - b1) * alpha
        )

    def render(self, cr: CairoContext, width: int, height: int, now_s: float) -> None:
        """Render the animation with phase-specific logic and color fading."""
        total_cycle = sum(self.phase_durations)
        if total_cycle == 0:
            # Handle edge case of zero total duration
            cr.set_source_rgb(*self.background)
            if hasattr(cr, 'paint'):
                cr.paint()
            return

        t = self._t % total_cycle
        max_radius = min(width, height) / 2
        fade_half = self.fade_duration / 2.0

        # Set background color
        cr.set_source_rgb(*self.background)
        if hasattr(cr, 'paint'):
            cr.paint()

        # Determine phase boundaries
        phase_ends = [0.0]
        for duration in self.phase_durations:
            phase_ends.append(phase_ends[-1] + duration)

        # Calculate radius and base color based on current phase
        if t <= phase_ends[1]:  # Phase 1: Inhale
            radius, base_color = self.phase1(t, max_radius)
        elif t <= phase_ends[2]:  # Phase 2: Hold
            radius, base_color = self.phase2(t, max_radius)
        elif t <= phase_ends[3]:  # Phase 3: Exhale
            radius, base_color = self.phase3(t, max_radius)
        else:  # Phase 4: Hold
            radius, base_color = self.phase4(t, max_radius)

        # Handle color fading at phase transitions
        color = base_color
        for i, end in enumerate(phase_ends[1:], 1):
            if t > end - fade_half and t < end + fade_half:
                alpha = (t - (end - fade_half)) / self.fade_duration
                prev_color = self.breath_color if i % 2 == 1 else self.hold_color
                next_color = self.hold_color if i % 2 == 1 else self.breath_color
                color = self.interpolate_color(prev_color, next_color, alpha)
                break
        if t < fade_half:  # Handle loop from end to beginning
            alpha = (t + fade_half) / self.fade_duration
            color = self.interpolate_color(self.hold_color, self.breath_color, alpha)

        # Render the circle
        cr.set_source_rgb(*color)
        cr.arc(width / 2, height / 2, radius, 0, 2 * math.pi)
        if hasattr(cr, 'fill'):
            cr.fill()

        # Render phase cue if active
        current_phase = 0
        for i, end in enumerate(phase_ends[1:]):
            if t <= end:
                current_phase = i
                break

        # Check if cue is enabled for current phase
        if self.phase_cues[current_phase] is not None:
            self._render_phase_cue(cr, current_phase, width, height)

    def _render_phase_cue(self, cr: CairoContext, phase_index: int, width: int, height: int) -> None:
        """
        Render a visual phase cue.

        Args:
            cr: Cairo context
            phase_index: Index of the current phase (0-3)
            width: Width of the rendering area
            height: Height of the rendering area
        """
        # Phase cue text mapping
        cue_text = {
            0: "Inhale", # Phase 1
            1: "Hold",   # Phase 2
            2: "Exhale", # Phase 3
            3: "Hold"    # Phase 4
        }

        # Skip if text cue not properly set
        if self.phase_cues[phase_index] != cue_text[phase_index]:
            return

        # Set up text rendering
        cr.set_source_rgb(1.0, 1.0, 1.0)  # White text

        # For a complete implementation, we would use Cairo text rendering functions:
        # Define constants for font slant and weight (these would normally come from cairo)
        FONT_SLANT_NORMAL = 0
        FONT_WEIGHT_BOLD = 1

        cr.select_font_face("Sans", FONT_SLANT_NORMAL, FONT_WEIGHT_BOLD)
        cr.set_font_size(48)

        # Ensure we have a valid text cue
        cue_text = self.phase_cues[phase_index]
        if cue_text is None:
            return

        x_bearing, y_bearing, text_width, text_height, _, _ = cr.text_extents(cue_text)
        x = 12 # width / 2 - text_width / 2
        y = height - 20 # height / 2 - text_height / 2 + 20
        cr.move_to(x, y)
        cr.show_text(cue_text)

        # For now, we'll just print the text to the console as a placeholder
        #print(f"Phase {phase_index + 1} cue: {self.phase_cues[phase_index]}")
