import math
from elevate.backend.animations.bouncy_ball import BouncyBallAnimation, SOFT_BLUE, LAVENDER, DEEP_INDIGO


class MockCairoContext:
    def __init__(self):
        self.calls = []

    def set_source_rgb(self, r, g, b):
        self.calls.append(('set_source_rgb', r, g, b))

    def rectangle(self, x, y, w, h):
        self.calls.append(('rectangle', x, y, w, h))

    def fill(self):
        self.calls.append(('fill',))

    def arc(self, xc, yc, radius, angle1, angle2):
        self.calls.append(('arc', xc, yc, radius, angle1, angle2))

    def paint(self):
        self.calls.append(('paint',))

    def select_font_face(self, family, slant, weight):
        self.calls.append(('select_font_face', family, slant, weight))

    def set_font_size(self, size):
        self.calls.append(('set_font_size', size))

    def text_extents(self, text):
        # Return mock text extents (x_bearing, y_bearing, width, height, x_advance, y_advance)
        return (0.0, 0.0, len(text) * 10.0, 20.0, len(text) * 10.0, 20.0)

    def move_to(self, x, y):
        self.calls.append(('move_to', x, y))

    def show_text(self, text):
        self.calls.append(('show_text', text))


def test_bouncy_ball_initialization():
    """Test BouncyBallAnimation initialization with default values."""
    anim = BouncyBallAnimation()
    
    assert anim.breath_color == SOFT_BLUE
    assert anim.hold_color == LAVENDER
    assert anim.background == DEEP_INDIGO
    assert anim._t == 0.0
    assert anim.phase_durations == (4.0, 4.0, 4.0, 4.0)
    assert anim.pulse_factor == 0.05
    assert anim.fade_duration == 0.5
    assert anim.phase_cues == ["Inhale", "Hold", "Exhale", "Hold"]


def test_bouncy_ball_custom_initialization():
    """Test BouncyBallAnimation initialization with custom values."""
    custom_breath = (0.1, 0.2, 0.3)
    custom_hold = (0.4, 0.5, 0.6)
    custom_bg = (0.7, 0.8, 0.9)
    
    anim = BouncyBallAnimation(
        breath_color=custom_breath,
        hold_color=custom_hold,
        background=custom_bg,
        pulse_factor=0.1,
        fade_duration=1.0
    )
    
    assert anim.breath_color == custom_breath
    assert anim.hold_color == custom_hold
    assert anim.background == custom_bg
    assert anim.pulse_factor == 0.1
    assert anim.fade_duration == 1.0


def test_bouncy_ball_reset():
    """Test the reset method."""
    anim = BouncyBallAnimation()
    anim._t = 5.0
    
    anim.reset()
    
    assert anim._t == 0.0


def test_bouncy_ball_set_breath_cycle():
    """Test setting breath cycle durations."""
    anim = BouncyBallAnimation()
    new_cycle = (2.0, 1.0, 3.0, 1.5)
    
    anim.set_breath_cycle(new_cycle)
    
    assert anim.phase_durations == new_cycle


def test_bouncy_ball_set_phase_cues():
    """Test setting phase cues."""
    anim = BouncyBallAnimation()
    new_cues = ("Breathe In", "Hold", "Breathe Out", None)
    
    anim.set_phase_cues(new_cues)
    
    assert anim.phase_cues == list(new_cues)


def test_bouncy_ball_is_phase_active():
    """Test phase active detection."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((2.0, 1.0, 2.0, 1.0))  # Total 6 seconds
    
    # Test phase 0 (0-2 seconds)
    assert anim.is_phase_active(0, 0.0) == True
    assert anim.is_phase_active(0, 1.0) == True
    assert anim.is_phase_active(0, 2.0) == False
    
    # Test phase 1 (2-3 seconds)
    assert anim.is_phase_active(1, 2.0) == True
    assert anim.is_phase_active(1, 2.5) == True
    assert anim.is_phase_active(1, 3.0) == False
    
    # Test phase 2 (3-5 seconds)
    assert anim.is_phase_active(2, 3.0) == True
    assert anim.is_phase_active(2, 4.0) == True
    assert anim.is_phase_active(2, 5.0) == False
    
    # Test phase 3 (5-6 seconds)
    assert anim.is_phase_active(3, 5.0) == True
    assert anim.is_phase_active(3, 5.5) == True
    assert anim.is_phase_active(3, 6.0) == False  # Wraps around
    
    # Test wraparound
    assert anim.is_phase_active(0, 6.0) == True  # 6 % 6 = 0
    assert anim.is_phase_active(0, 7.0) == True  # 7 % 6 = 1


def test_bouncy_ball_is_phase_active_zero_duration():
    """Test phase active detection with zero total duration."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((0.0, 0.0, 0.0, 0.0))
    
    assert anim.is_phase_active(0, 0.0) == False
    assert anim.is_phase_active(1, 1.0) == False
    assert anim.is_phase_active(2, 2.0) == False
    assert anim.is_phase_active(3, 3.0) == False


def test_bouncy_ball_update():
    """Test the update method."""
    anim = BouncyBallAnimation()
    initial_time = anim._t
    
    anim.update(0.1, 100, 100)
    
    assert anim._t == initial_time + 0.1


def test_bouncy_ball_phase1():
    """Test phase 1 (inhale) calculations."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((2.0, 1.0, 2.0, 1.0))
    max_radius = 50.0
    
    # At start of phase
    radius, color = anim.phase1(0.0, max_radius)
    assert radius == 0.0
    assert color == SOFT_BLUE
    
    # Mid phase
    radius, color = anim.phase1(1.0, max_radius)
    expected_radius = (1.0 / 2.0) * max_radius * (1.0 - anim.pulse_factor)
    assert abs(radius - expected_radius) < 0.001
    assert color == SOFT_BLUE
    
    # At end of phase
    radius, color = anim.phase1(2.0, max_radius)
    expected_radius = max_radius * (1.0 - anim.pulse_factor)
    assert abs(radius - expected_radius) < 0.001
    assert color == SOFT_BLUE


def test_bouncy_ball_phase1_zero_duration():
    """Test phase 1 with zero duration."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((0.0, 1.0, 2.0, 1.0))
    max_radius = 50.0
    
    radius, color = anim.phase1(0.0, max_radius)
    assert radius == 0.0
    assert color == SOFT_BLUE


def test_bouncy_ball_phase2():
    """Test phase 2 (hold) calculations."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((2.0, 1.0, 2.0, 1.0))
    max_radius = 50.0
    
    # Test pulsation behavior
    radius, color = anim.phase2(2.1, max_radius)  # 0.1 seconds into hold phase
    assert color == LAVENDER
    
    # Test that radius is within expected range
    min_radius = max_radius * (1.0 - anim.pulse_factor)
    assert min_radius <= radius <= max_radius


def test_bouncy_ball_phase3():
    """Test phase 3 (exhale) calculations."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((2.0, 1.0, 2.0, 1.0))
    max_radius = 50.0
    
    # At start of phase (t=3.0)
    radius, color = anim.phase3(3.0, max_radius)
    expected_radius = max_radius * (1.0 - anim.pulse_factor)
    assert abs(radius - expected_radius) < 0.001
    assert color == SOFT_BLUE
    
    # Mid phase
    radius, color = anim.phase3(4.0, max_radius)
    expected_radius = 0.5 * max_radius * (1.0 - anim.pulse_factor)
    assert abs(radius - expected_radius) < 0.001
    assert color == SOFT_BLUE
    
    # At end of phase
    radius, color = anim.phase3(5.0, max_radius)
    assert radius == 0.0
    assert color == SOFT_BLUE


def test_bouncy_ball_phase3_zero_duration():
    """Test phase 3 with zero duration."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((2.0, 1.0, 0.0, 1.0))
    max_radius = 50.0
    
    radius, color = anim.phase3(3.0, max_radius)
    assert radius == 0.0
    assert color == SOFT_BLUE


def test_bouncy_ball_phase4():
    """Test phase 4 (hold) calculations."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((2.0, 1.0, 2.0, 1.0))
    max_radius = 50.0
    
    # At start of phase (t=5.0)
    radius, color = anim.phase4(5.0, max_radius)
    # Should be pulsating around max_radius * pulse_factor
    assert color == LAVENDER
    
    # Test that radius is within expected range (0 to max_radius * pulse_factor)
    max_expected_radius = max_radius * anim.pulse_factor
    assert 0 <= radius <= max_expected_radius


def test_bouncy_ball_interpolate_color():
    """Test color interpolation."""
    anim = BouncyBallAnimation()
    
    # Test interpolation at start
    color = anim.interpolate_color((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 0.0)
    assert color == (0.0, 0.0, 0.0)
    
    # Test interpolation at end
    color = anim.interpolate_color((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 1.0)
    assert color == (1.0, 1.0, 1.0)
    
    # Test interpolation at midpoint
    color = anim.interpolate_color((0.0, 0.0, 0.0), (1.0, 1.0, 1.0), 0.5)
    assert color == (0.5, 0.5, 0.5)


def test_bouncy_ball_render_zero_duration():
    """Test render with zero total duration."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((0.0, 0.0, 0.0, 0.0))
    cr = MockCairoContext()
    
    anim.render(cr, 100, 100, 0.0)
    
    # Should just paint background
    assert len([call for call in cr.calls if call[0] == 'set_source_rgb']) >= 1
    assert len([call for call in cr.calls if call[0] == 'paint']) >= 1


def test_bouncy_ball_render_normal_cycle():
    """Test render with normal cycle."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((1.0, 0.5, 1.0, 0.5))  # 3 second cycle
    cr = MockCairoContext()
    
    # Test at different times
    anim._t = 0.5  # In phase 1
    anim.render(cr, 100, 100, 0.0)
    
    # Should have set colors and drawn arc
    assert len([call for call in cr.calls if call[0] == 'set_source_rgb']) >= 1
    assert len([call for call in cr.calls if call[0] == 'arc']) >= 1


def test_bouncy_ball_render_with_phase_cues():
    """Test render with phase cues enabled."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((1.0, 0.5, 1.0, 0.5))
    cr = MockCairoContext()
    
    # Test at time when phase 1 cue should show
    anim._t = 0.5  # In phase 1 (Inhale)
    anim.render(cr, 100, 100, 0.0)
    
    # Should have text rendering calls
    font_calls = [call for call in cr.calls if call[0] in ('select_font_face', 'set_font_size', 'move_to', 'show_text')]
    assert len(font_calls) >= 3  # Should have at least font setup and text rendering


def test_bouncy_ball_render_phase_transitions():
    """Test render during phase transitions with color fading."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((0.5, 0.5, 0.5, 0.5))  # 2 second cycle
    cr = MockCairoContext()
    
    # Test near end of phase 1 (transition to phase 2)
    anim._t = 0.4  # Near end of phase 1
    anim.render(cr, 100, 100, 0.0)
    
    # Should have set colors for transition
    color_calls = [call for call in cr.calls if call[0] == 'set_source_rgb']
    assert len(color_calls) >= 1


def test_bouncy_ball_render_loop_transition():
    """Test render during loop transition (end to beginning)."""
    anim = BouncyBallAnimation()
    anim.set_breath_cycle((0.5, 0.5, 0.5, 0.5))  # 2 second cycle
    cr = MockCairoContext()
    
    # Test near end of cycle (transition to beginning)
    anim._t = 1.9  # Near end of cycle
    anim.render(cr, 100, 100, 0.0)
    
    # Should have set colors for transition
    color_calls = [call for call in cr.calls if call[0] == 'set_source_rgb']
    assert len(color_calls) >= 1