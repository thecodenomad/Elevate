from __future__ import annotations

import math
from .base import Animation, CairoContext


class ColorLayersAnimation(Animation):
    def __init__(self) -> None:
        self._t = 0.0
        self._cycle = (4.0, 4.0, 4.0, 4.0)

    def set_breath_cycle(self, cycle: tuple[float, float, float, float]) -> None:
        self._cycle = cycle

    def reset(self) -> None:
        self._t = 0.0

    def update(self, dt: float, width: int, height: int) -> None:
        self._t += dt
        total = sum(self._cycle)
        if total > 0:
            self._t %= total

    def render(self, cr: CairoContext, width: int, height: int, now_s: float) -> None:
        inhale, hold1, exhale, hold2 = self._cycle
        total = max(1.0, inhale + hold1 + exhale + hold2)
        t = self._t % total

        if t < inhale:
            frac = t / inhale if inhale > 0 else 1.0
            phase = frac
        elif t < inhale + hold1:
            phase = 1.0
        elif t < inhale + hold1 + exhale:
            ex_t = t - inhale - hold1
            frac = ex_t / exhale if exhale > 0 else 1.0
            phase = 1.0 - frac
        else:
            phase = 0.0

        red = phase
        green = 1.0 - phase
        blue = 0.5 + 0.5 * phase
        cr.set_source_rgb(red, green, blue)
        cr.rectangle(0, 0, width, height)
        cr.fill()
