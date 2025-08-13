from elevate.backend.animations import get_animation_class
from elevate.backend.animations.base import Animation
from elevate.backend.animations.bouncy_ball import BouncyBallAnimation


class Dummy(Animation):
    def __init__(self):
        self.r = []

    def reset(self):
        self.r.append("reset")

    def update(self, dt: float, width: int, height: int) -> None:
        self.r.append(("u", dt, width, height))

    def render(self, cr, width: int, height: int, now_s: float) -> None:
        self.r.append(("r", width, height, now_s))


def test_get_animation_class_by_name_and_number_defaults():
    assert get_animation_class("color").__name__
    assert get_animation_class("1").__name__
    # digit mapping 2 -> ball
    assert get_animation_class("2").__name__ == BouncyBallAnimation.__name__
    # default fallback
    assert get_animation_class("unknown").__name__ == get_animation_class("color").__name__


def test_base_set_breath_cycle_noop():
    d = Dummy()
    d.set_breath_cycle((1, 1, 1, 1))
    d.update(0.0, 0, 0)
    class _C:
        def set_source_rgb(self, r: float, g: float, b: float): pass
        def rectangle(self, x: float, y: float, w: float, h: float): pass
        def fill(self): pass
        def arc(self, xc: float, yc: float, radius: float, angle1: float, angle2: float): pass
        def paint(self): pass
        def select_font_face(self, family: str, slant: int, weight: int): pass
        def set_font_size(self, size: float): pass
        def text_extents(self, text: str) -> tuple: return (0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
        def move_to(self, x: float, y: float): pass
        def show_text(self, text: str): pass
    d.render(_C(), 0, 0, 0.0)
    assert d.r and d.r[0] == ("u", 0.0, 0, 0)


class CR:
    def __init__(self):
        self.ops = []

    def set_source_rgb(self, r, g, b):
        self.ops.append(("c", r, g, b))

    def rectangle(self, x, y, w, h):
        self.ops.append(("rect", x, y, w, h))

    def fill(self):
        self.ops.append(("fill",))

    def arc(self, xc: float, yc: float, radius: float, angle1: float, angle2: float):
        self.ops.append(("arc", xc, yc, radius, angle1, angle2))

    def paint(self):
        self.ops.append(("paint",))

    def select_font_face(self, family: str, slant: int, weight: int) -> None:
        self.ops.append(("font_face", family, slant, weight))

    def set_font_size(self, size: float) -> None:
        self.ops.append(("font_size", size))

    def text_extents(self, text: str) -> tuple:
        # Return mock text extents (x_bearing, y_bearing, width, height, x_advance, y_advance)
        return (0.0, 0.0, len(text) * 10.0, 20.0, len(text) * 10.0, 20.0)

    def move_to(self, x: float, y: float) -> None:
        self.ops.append(("move_to", x, y))

    def show_text(self, text: str) -> None:
        self.ops.append(("show_text", text))


def test_bouncy_ball_all_branches():
    a = BouncyBallAnimation()
    a.set_breath_cycle((0.2, 0.1, 0.2, 0.1))
    cr = CR()

    # inhale
    a.reset(); a.update(0.1, 100, 100); a.render(cr, 100, 100, 0.0)
    # hold1
    a.update(0.2, 100, 100); a.render(cr, 100, 100, 0.0)
    # exhale
    a.update(0.2, 100, 100); a.render(cr, 100, 100, 0.0)
    # hold2
    a.update(0.2, 100, 100); a.render(cr, 100, 100, 0.0)

    arcs = [op for op in cr.ops if op[0] == "arc"]
    assert len(arcs) >= 4
