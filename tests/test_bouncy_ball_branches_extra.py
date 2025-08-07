from src.backend.animations.bouncy_ball import BouncyBallAnimation

class CR:
    def set_source_rgb(self, r: float, g: float, b: float): pass
    def rectangle(self, x: float, y: float, w: float, h: float): pass
    def fill(self): pass
    def arc(self, xc: float, yc: float, radius: float, angle1: float, angle2: float): pass


def test_bouncy_ball_zero_total_guard_and_else_branch():
    a = BouncyBallAnimation()
    a.set_breath_cycle((0.0, 0.0, 0.0, 0.0))
    cr = CR()
    a.reset()
    a.update(0.05, 100, 100)
    a.render(cr, 100, 100, 0.0)

    # Now use a cycle that lands in the final else branch (hold2)
    a.set_breath_cycle((0.1, 0.1, 0.1, 0.5))
    a.reset()
    a.update(0.45, 100, 100)  # inhale+hold1+exhale=0.3, so t=0.45 in hold2
    a.render(cr, 100, 100, 0.0)
