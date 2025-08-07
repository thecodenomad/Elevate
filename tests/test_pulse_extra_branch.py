from src.backend.animations.pulse import PulseAnimation

class CR:
    def set_source_rgb(self, r: float, g: float, b: float): pass
    def rectangle(self, x: float, y: float, w: float, h: float): pass
    def fill(self): pass
    def arc(self, xc: float, yc: float, radius: float, angle1: float, angle2: float): pass


def test_pulse_hold2_branch():
    a = PulseAnimation()
    a.set_breath_cycle((0.1, 0.1, 0.1, 0.5))
    cr = CR()
    a.reset()
    a.update(0.45, 100, 100)
    a.render(cr, 100, 100, 0.0)
