from __future__ import annotations

import math
from typing import Tuple

from .base import Animation, CairoContext


class BouncyBallAnimation(Animation):
    def __init__(self) -> None:
        self._cycle: Tuple[float, float, float, float] = (4.0, 4.0, 4.0, 4.0)
        self._t = 0.0
        self.pulse_factor = .05
        self.breath_color = (0.2, 0.6, 0.9)
        self.hold_color = (0.6, 0.4, 0.8)
        self.background_color = (0.2, 0.2, 0.6)


        print("Bouncy instantiated")

    def set_breath_cycle(self, cycle: Tuple[float, float, float, float]) -> None:
        self._cycle = (4.0, 4.0, 4.0, 4.0)

    def reset(self) -> None:
        self._t = 0.0

    def update(self, dt: float, width: int, height: int) -> None:
        self._cycle = (4.0, 4.0, 4.0, 4.0)
        self._t += dt
        total = 16.0
        if total > 0:
            self._t %= total

    def render(self, cr: CairoContext, width: int, height: int, now_s: float) -> None:
        inhale, hold1, exhale, hold2 = (4.0, 4.0, 4.0, 4.0)
        total = 16.0
        t = self._t % total
        max_radius = min(width, height) / 2
        pulse_factor_phase2 = 0.05
        pulse_factor_phase4 = 0.025
        fade_duration = 0.5  # Total fade duration in seconds
        fade_half = fade_duration / 2.0  # Fade starts/ends this many seconds before/after transition

        # Set background color using self.background
        cr.set_source_rgb(*self.background_color)  # Deep Indigo (0.2, 0.2, 0.6)
        cr.paint()

        # Helper function to interpolate between two RGB colors
        def interpolate_color(color1, color2, alpha):
            r1, g1, b1 = color1
            r2, g2, b2 = color2
            return (
                r1 + (r2 - r1) * alpha,
                g1 + (g2 - g1) * alpha,
                b1 + (b2 - b1) * alpha
            )

        # Determine radius and base colors for each phase
        if t <= 4.0:
            # Phase 1: Growing from 0 to max_radius * (1 - pulse_factor_phase2)
            radius = (t / 4.0) * max_radius * (1.0 - pulse_factor_phase2)
            base_color = self.breath_color  # Soft Blue (0.2, 0.6, 0.9)
            next_color = self.hold_color if t > 4.0 - fade_half else base_color
        elif t <= 8.0:
            # Phase 2: Pulsating between max_radius * (1 - pulse_factor_phase2) and max_radius
            pulse_time = t - 4.0
            pulse = 0.5 * (1.0 + math.cos(2.0 * math.pi * pulse_time / 1.0 + math.pi))  # Period of 1 second
            min_radius = max_radius * (1.0 - pulse_factor_phase2)
            radius = min_radius + (max_radius - min_radius) * pulse
            base_color = self.hold_color  # Pale Lavender (0.6, 0.4, 0.8)
            next_color = self.breath_color if t > 8.0 - fade_half else base_color
        elif t <= 12.0:
            # Phase 3: Shrinking from max_radius * (1 - pulse_factor_phase2) to 0
            radius = (1.0 - ((t - 8.0) / 4.0)) * max_radius * (1.0 - pulse_factor_phase2)
            base_color = self.breath_color  # Soft Blue (0.2, 0.6, 0.9)
            next_color = self.hold_color if t > 12.0 - fade_half else base_color
        else:
            # Phase 4: Pulsating between 0 and max_radius * pulse_factor_phase4
            pulse_time = t - 12.0
            pulse = 0.5 * (1.0 + math.cos(2.0 * math.pi * pulse_time / 1.0 + math.pi))  # Period of 1 second
            radius = max_radius * pulse_factor_phase4 * pulse
            base_color = self.hold_color  # Pale Lavender (0.6, 0.4, 0.8)
            next_color = self.breath_color if t > 16.0 - fade_half else base_color

        # Handle color fading at phase transitions
        if t < fade_half:  # Near t=0 (loop from t=16)
            alpha = (t + fade_half) / fade_duration
            color = interpolate_color(self.hold_color, self.breath_color, alpha)
        elif t > 4.0 - fade_half and t < 4.0 + fade_half:  # Near t=4
            alpha = (t - (4.0 - fade_half)) / fade_duration
            color = interpolate_color(self.breath_color, self.hold_color, alpha)
        elif t > 8.0 - fade_half and t < 8.0 + fade_half:  # Near t=8
            alpha = (t - (8.0 - fade_half)) / fade_duration
            color = interpolate_color(self.hold_color, self.breath_color, alpha)
        elif t > 12.0 - fade_half and t < 12.0 + fade_half:  # Near t=12
            alpha = (t - (12.0 - fade_half)) / fade_duration
            color = interpolate_color(self.breath_color, self.hold_color, alpha)
        elif t > 16.0 - fade_half:  # Near t=16
            alpha = (t - (16.0 - fade_half)) / fade_duration
            color = interpolate_color(self.hold_color, self.breath_color, alpha)
        else:
            color = base_color

        cr.set_source_rgb(*color)
        cr.arc(width / 2, height / 2, radius, 0, 6.283185307179586)
        cr.fill()
