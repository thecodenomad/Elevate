from __future__ import annotations

from typing import Tuple

from .base import Animation, CairoContext


class BouncyBallAnimation(Animation):
    def __init__(self) -> None:
        self._cycle: Tuple[float, float, float, float] = (4.0, 4.0, 4.0, 4.0)
        self._t = 0.0

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

        if t < 4.0:
            radius = (t / 4.0) * max_radius
        elif t < 8.0:
            radius = max_radius
        elif t < 12.0:
            radius = (1.0 - ((t - 8.0) / 4.0)) * max_radius
        else:
            radius = 0.0

        cr.set_source_rgb(0.2, 0.6, 0.9)
        cr.arc(width / 2, height / 2, radius, 0, 6.283185307179586)
        cr.fill()
