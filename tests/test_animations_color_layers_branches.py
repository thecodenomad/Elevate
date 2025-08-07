from src.backend.animations.color_layers import ColorLayersAnimation

class CR:
    def __init__(self): self.ops=[]
    def set_source_rgb(self, r: float, g: float, b: float): self.ops.append((r,g,b))
    def rectangle(self, x: float, y: float, w: float, h: float): pass
    def fill(self): pass
    def arc(self, xc: float, yc: float, radius: float, angle1: float, angle2: float): pass


def test_color_layers_all_phases():
    a = ColorLayersAnimation()
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
    assert len(cr.ops) >= 4
