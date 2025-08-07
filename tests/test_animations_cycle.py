import math
import types

from src.backend.animations.pulse import PulseAnimation
from src.backend.animations.color_layers import ColorLayersAnimation
from src.backend.animations.bouncy_ball import BouncyBallAnimation


class MockCairo:
    def __init__(self):
        self.ops = []

    def set_source_rgb(self, r, g, b):
        self.ops.append(("set_source_rgb", round(r,3), round(g,3), round(b,3)))

    def rectangle(self, x, y, w, h):
        self.ops.append(("rectangle", x, y, w, h))

    def fill(self):
        self.ops.append(("fill",))

    def arc(self, xc: float, yc: float, radius: float, angle1: float, angle2: float):
        self.ops.append(("arc", xc, yc, round(radius,3), angle1, angle2))


def step(anim, seconds, width=200, height=100):
    t = 0.0
    while t < seconds:
        dt = min(0.05, seconds - t)
        anim.update(dt, width, height)
        t += dt


def test_pulse_uses_cycle_and_renders_all_phases():
    a = PulseAnimation()
    a.set_breath_cycle((0.2, 0.1, 0.2, 0.1))
    cr = MockCairo()

    # inhale
    step(a, 0.1)
    a.render(cr, 100, 100, 0.0)
    # hold1
    step(a, 0.2)
    a.render(cr, 100, 100, 0.0)
    # exhale
    step(a, 0.2)
    a.render(cr, 100, 100, 0.0)
    # hold2
    step(a, 0.2)
    a.render(cr, 100, 100, 0.0)

    assert any(op[0]=="arc" for op in cr.ops)
    # ensure cycle wraps
    step(a, 1.0)
    a.render(cr, 100, 100, 0.0)


def test_color_layers_responds_to_cycle():
    a = ColorLayersAnimation()
    a.set_breath_cycle((0.2, 0.1, 0.2, 0.1))
    cr = MockCairo()

    step(a, 0.05)
    a.render(cr, 50, 50, 0.0)
    step(a, 0.3)
    a.render(cr, 50, 50, 0.0)
    # more cycles to hit branches
    step(a, 1.0)
    a.render(cr, 50, 50, 0.0)

    colors = [op for op in cr.ops if op[0]=="set_source_rgb"]
    assert len(colors) >= 2
    assert colors[0] != colors[-1]


def test_bouncy_ball_cycle_and_reset():
    a = BouncyBallAnimation()
    a.set_breath_cycle((0.2, 0.1, 0.2, 0.1))
    cr = MockCairo()

    step(a, 0.15)
    a.render(cr, 80, 60, 0.0)
    a.reset()
    step(a, 0.05)
    a.render(cr, 80, 60, 0.0)

    arcs = [op for op in cr.ops if op[0]=="arc"]
    assert arcs, "expected arcs to be drawn"
