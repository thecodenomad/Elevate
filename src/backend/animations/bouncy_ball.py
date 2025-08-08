from __future__ import annotations

import math
from typing import Tuple

from .base import Animation, CairoContext

SOFT_BLUE = (0.2, 0.6, 0.9)
LAVENDER = (0.6, 0.4, 0.8)
DEEP_INDIGO = (0.2, 0.2, 0.6)

class BouncyBallAnimation(Animation):
    def __init__(self, breath_color: tuple[float, float, float] = SOFT_BLUE, hold_color: tuple[float, float, float] = LAVENDER, background: tuple[float, float, float] = DEEP_INDIGO, pulse_factor: float = 0.05, fade_duration: float = 0.5) -> None:
        self.breath_color = breath_color  # Soft Blue for inhale/exhale
        self.hold_color = hold_color      # Pale Lavender for hold phases
        self.background = background      # Deep Indigo for background
        self._t = 0.0
        self.phase_durations = (4.0, 4.0, 4.0, 4.0)  # Inhale, hold1, exhale, hold2
        self.pulse_factor_phase2 = pulse_factor
        self.pulse_factor_phase4 = pulse_factor / 2
        self.fade_duration = fade_duration  # Total fade duration in seconds

    def reset(self) -> None:
        """Reset the animation to its initial state."""
        self._t = 0.0

    def set_breath_cycle(self, cycle: Tuple[float, float, float, float]) -> None:
        """Set the duration of each phase (inhale, hold1, exhale, hold2)."""
        self.phase_durations = cycle

    def update(self, dt: float, width: int, height: int) -> None:
        """Update the animation state based on elapsed time."""
        self._t += dt

    def phase1(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 1: Inhale - Growing from 0 to max_radius * (1 - pulse_factor_phase2)."""
        radius = (t / self.phase_durations[0]) * max_radius * (1.0 - self.pulse_factor_phase2)
        return radius, self.breath_color

    def phase2(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 2: Hold - Pulsating between max_radius * (1 - pulse_factor_phase2) and max_radius."""
        pulse_time = t - self.phase_durations[0]
        pulse = 0.5 * (1.0 + math.cos(2.0 * math.pi * pulse_time / 1.0 + math.pi))  # Period of 1 second
        min_radius = max_radius * (1.0 - self.pulse_factor_phase2)
        radius = min_radius + (max_radius - min_radius) * pulse
        return radius, self.hold_color

    def phase3(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 3: Exhale - Shrinking from max_radius * (1 - pulse_factor_phase2) to 0."""
        phase_start = sum(self.phase_durations[:2])
        radius = (1.0 - ((t - phase_start) / self.phase_durations[2])) * max_radius * (1.0 - self.pulse_factor_phase2)
        return radius, self.breath_color

    def phase4(self, t: float, max_radius: float) -> tuple[float, tuple[float, float, float]]:
        """Phase 4: Hold - Pulsating between 0 and max_radius * pulse_factor_phase4."""
        phase_start = sum(self.phase_durations[:3])
        pulse_time = t - phase_start
        pulse = 0.5 * (1.0 + math.cos(2.0 * math.pi * pulse_time / 1.0 + math.pi))  # Period of 1 second
        radius = max_radius * self.pulse_factor_phase4 * pulse
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
        total = sum(self.phase_durations)
        t = self._t % total
        max_radius = min(width, height) / 2
        fade_half = self.fade_duration / 2.0

        # Set background color
        cr.set_source_rgb(*self.background)
        cr.paint()

        # Determine phase boundaries
        phase_ends = [0.0]
        for duration in self.phase_durations:
            phase_ends.append(phase_ends[-1] + duration)

        # Calculate radius and base color based on current phase
        if t <= phase_ends[1]:
            radius, base_color = self.phase1(t, max_radius)
            next_color = self.hold_color if t > phase_ends[1] - fade_half else base_color
        elif t <= phase_ends[2]:
            radius, base_color = self.phase2(t, max_radius)
            next_color = self.breath_color if t > phase_ends[2] - fade_half else base_color
        elif t <= phase_ends[3]:
            radius, base_color = self.phase3(t, max_radius)
            next_color = self.hold_color if t > phase_ends[3] - fade_half else base_color
        else:
            radius, base_color = self.phase4(t, max_radius)
            next_color = self.breath_color if t > phase_ends[4] - fade_half else base_color

        # Handle color fading at phase transitions
        color = base_color
        for i, end in enumerate(phase_ends[1:], 1):
            if t > end - fade_half and t < end + fade_half:
                alpha = (t - (end - fade_half)) / self.fade_duration
                prev_color = self.breath_color if i % 2 == 1 else self.hold_color
                next_color = self.hold_color if i % 2 == 1 else self.breath_color
                color = self.interpolate_color(prev_color, next_color, alpha)
                break
        if t < fade_half:  # Handle loop from t=16 to t=0
            alpha = (t + fade_half) / self.fade_duration
            color = self.interpolate_color(self.hold_color, self.breath_color, alpha)

        cr.set_source_rgb(*color)
        cr.arc(width / 2, height / 2, radius, 0, 6.283185307179586)
        cr.fill()
