"""Extended tests for VisualStimulus covering animation loop and rendering logic."""

import builtins
from unittest.mock import MagicMock, patch

import pytest

from elevate.backend.visual_stimulus import VisualStimulus
from elevate.backend.animations.base import Animation
from elevate.backend.animations import _REGISTRY


class DummyAnimation(Animation):
    """Simple animation that records calls for testing."""

    def __init__(self):
        self.updated = []
        self.rendered = []
        self.reset_called = False

    def reset(self):
        self.reset_called = True

    def update(self, dt: float, width: int, height: int) -> None:
        self.updated.append((dt, width, height))

    def render(self, cr, width: int, height: int, now_s: float) -> None:
        self.rendered.append((cr, width, height, now_s))


@pytest.fixture(autouse=True)
def patch_animation_registry():
    """Patch the animation registry to return DummyAnimation for any name."""
    with patch.dict(_REGISTRY, {"color": DummyAnimation}, clear=False):
        yield


def test_play_initializes_animation_and_starts_loop(monkeypatch):
    vs = VisualStimulus()
    vs.stimuli_type = 0  # Use integer instead of string
    # Ensure visual stimuli are enabled
    vs.enable_visual_stimuli = True

    # Simulate a widget with required methods
    widget = MagicMock()
    alloc = MagicMock()
    alloc.width = 200
    alloc.height = 100
    widget.get_allocation.return_value = alloc
    widget.queue_draw = MagicMock()
    vs.set_widget(widget)

    # Mock GLib.timeout_add to capture the callback
    callback_holder = {}
    def fake_timeout_add(interval, callback):
        # store the callback for later invocation
        callback_holder["cb"] = callback
        return 123  # dummy source id
    monkeypatch.setattr("gi.repository.GLib.timeout_add", fake_timeout_add)
    monkeypatch.setattr("gi.repository.GLib.source_remove", lambda src: None)
    # Mock get_monotonic_time to return a predictable sequence
    times = [1_000_000.0, 1_000_000_010.0]  # 10 milliseconds later
    monkeypatch.setattr("gi.repository.GLib.get_monotonic_time", lambda: times.pop(0))

    # Call play – should set _is_playing and schedule animation
    vs.play()
    assert vs._is_playing is True
    assert vs._animation_source == 123
    # The animation instance should be a DummyAnimation
    assert isinstance(vs._animation, DummyAnimation)

    # Invoke the stored animation callback
    # It should call update on the dummy animation and queue_draw
    cb = callback_holder.get("cb")
    assert cb is not None
    result = cb()
    # The callback should return GLib.SOURCE_CONTINUE (value 1)
    assert result == 1
    # Verify update called with dt approx 0.1 (10 milliseconds / 100)
    assert vs._animation.updated, "Animation update not called"
    dt, w, h = vs._animation.updated[0]
    assert pytest.approx(dt, rel=1e-3) == 0.1
    assert w == 200 and h == 100
    widget.queue_draw.assert_called_once()


def test_pause_stops_animation_and_resets_time(monkeypatch):
    vs = VisualStimulus()
    vs.enable_visual_stimuli = True
    vs.stimuli_type = 0  # Use integer instead of string

    # Simulate a widget to enable animation
    widget = MagicMock()
    alloc = MagicMock()
    alloc.width = 200
    alloc.height = 100
    widget.get_allocation.return_value = alloc
    widget.queue_draw = MagicMock()
    vs.set_widget(widget)

    # Mock GLib functions
    monkeypatch.setattr("gi.repository.GLib.timeout_add", lambda i, cb: 999)
    source_remove_mock = MagicMock()
    monkeypatch.setattr("gi.repository.GLib.source_remove", source_remove_mock)

    vs.play()
    assert vs._is_playing is True
    # Simulate some time accumulation
    vs._time = 5.0
    vs.pause()
    assert vs._is_playing is False
    assert vs._time == 0.0
    # Ensure source_remove was called
    source_remove_mock.assert_called_with(999)


def test_render_calls_animation_render_when_playing(monkeypatch):
    vs = VisualStimulus()
    vs.enable_visual_stimuli = True
    vs.stimuli_type = 0  # Use integer instead of string
    # Mock GLib.get_monotonic_time to keep time stable
    monkeypatch.setattr("gi.repository.GLib.get_monotonic_time", lambda: 0)
    # Ensure animation is created lazily on render
    cr = MagicMock()
    cr.set_source_rgb = MagicMock()
    cr.rectangle = MagicMock()
    cr.fill = MagicMock()
    # Not playing – should draw background only
    vs.render(None, cr, 10, 10)
    cr.set_source_rgb.assert_called_once_with(0.1, 0.1, 0.1)
    cr.rectangle.assert_called_once_with(0, 0, 10, 10)
    cr.fill.assert_called_once()
    # Now start playing and render again
    cr.reset_mock()
    vs.play()
    # Simulate widget for _animate (not needed for render directly)
    vs._animation = DummyAnimation()
    vs._is_playing = True
    vs._time = 2.5
    vs.render(None, cr, 20, 30)
    # Dummy animation's render should have been called with accumulated time
    assert vs._animation.rendered, "Animation render not called"
    _, w, h, now = vs._animation.rendered[0]
    assert w == 20 and h == 30 and now == 2.5


def test_render_background_when_disabled(monkeypatch):
    vs = VisualStimulus()
    cr = MagicMock()
    cr.set_source_rgb = MagicMock()
    cr.rectangle = MagicMock()
    cr.fill = MagicMock()
    # Visual stimuli disabled – should draw simple background
    vs.render(None, cr, 5, 5)
    cr.set_source_rgb.assert_called_once_with(0.1, 0.1, 0.1)
    cr.rectangle.assert_called_once_with(0, 0, 5, 5)
    cr.fill.assert_called_once()
