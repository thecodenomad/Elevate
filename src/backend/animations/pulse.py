from __future__ import annotations

import math
from .base import Animation, CairoContext


class PulseAnimation(Animation):
    def __init__(self) -> None:
        self._phase = 0.0
        self._cycle = (4.0, 4.0, 4.0, 4.0)

    def reset(self) -> None:
        self._phase = 0.0

    def set_breath_cycle(self, cycle: tuple[float, float, float, float]) -> None:
        self._cycle = cycle

    def update(self, dt: float, width: int, height: int) -> None:
        self._phase += dt
        total = sum(self._cycle)
        if total > 0:
            self._phase %= total

    def render(self, cr: CairoContext, width: int, height: int, now_s: float) -> None:
        inhale, hold1, exhale, hold2 = self._cycle
        total = max(1.0, inhale + hold1 + exhale + hold2)
        t = self._phase % total
        max_radius = min(width, height) / 2

        if t < inhale:
            frac = t / inhale if inhale > 0 else 1.0
            radius = frac * max_radius
        elif t < inhale + hold1:
            radius = max_radius
        elif t < inhale + hold1 + exhale:
            ex_t = t - inhale - hold1
            frac = ex_t / exhale if exhale > 0 else 1.0
            radius = (1.0 - frac) * max_radius
        else:
            radius = 0.0

        cr.set_source_rgb(0.2, 0.4, 0.8)
        cr.arc(width / 2, height / 2, radius, 0, 2 * math.pi)
        cr.fill()
