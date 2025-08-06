import types
import math
import pytest
from src.backend.visual_stimulus import VisualStimulus


class MockCR:
    def __init__(self):
        self.ops = []
    def set_source_rgb(self, r, g, b):
        self.ops.append(("color", round(r,3), round(g,3), round(b,3)))
    def rectangle(self, x, y, w, h):
        self.ops.append(("rect", x, y, w, h))
    def fill(self):
        self.ops.append(("fill",))
    def arc(self, x, y, r, a1, a2):
        self.ops.append(("arc", x, y, round(r,2), a1, a2))


class MockWidget:
    def __init__(self):
        self.draws = 0
    def queue_draw(self):
        self.draws += 1


def test_render_inactive_draws_background():
    v = VisualStimulus()
    cr = MockCR()
    v.render(None, cr, 100, 50)
    assert ("rect", 0, 0, 100, 50) in cr.ops
    assert ("fill",) in cr.ops


def test_render_color_branch():
    v = VisualStimulus()
    v.set_enable_visual_stimuli(True)
    v.set_stimuli_type(0)
    v._is_playing = True
    cr = MockCR()
    v.render(None, cr, 100, 50)
    # Should have a rectangle and fill
    assert any(op[0] == "rect" for op in cr.ops)
    assert any(op[0] == "fill" for op in cr.ops)


def test_render_breath_branch():
    v = VisualStimulus()
    v.set_enable_visual_stimuli(True)
    v.set_stimuli_type(1)
    v._is_playing = True
    cr = MockCR()
    v.render(None, cr, 120, 120)
    # Should draw an arc (circle) and fill
    assert any(op[0] == "arc" for op in cr.ops)
    assert any(op[0] == "fill" for op in cr.ops)


def test_play_pause_stop_transitions():
    v = VisualStimulus()
    w = MockWidget()
    v.set_widget(w)
    v.set_enable_visual_stimuli(True)
    assert v._is_playing is False
    v.play()
    assert v._is_playing is True
    v.pause()
    assert v._is_playing is False
    v.play()
    v.stop()
    assert v._is_playing is False


def test_widget_queue_draw_called_by_animate_when_playing(monkeypatch):
    v = VisualStimulus()
    w = MockWidget()
    v.set_widget(w)
    v.set_enable_visual_stimuli(True)
    v._is_playing = True
    # Call internal animate once; should queue draw
    cont = v._animate()
    assert cont != 0
    assert w.draws >= 1


def test_getters_setters_roundtrip():
    v = VisualStimulus()
    v.set_enable_visual_stimuli(True)
    v.set_stimuli_type(1)
    assert v.get_enable_visual_stimuli() is True
    assert v.get_stimuli_type() == 1
