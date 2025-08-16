import pytest
from elevate.backend.state_induction_controller import StateInductionController
from elevate.settings import ElevateSettings

@pytest.fixture
def settings():
    """Fixture to create an ElevateSettings instance with a mock GSettings schema."""
    try:
        settings = ElevateSettings()
        print(settings.__dict__)
        return settings
    except GLib.Error as e:
        pytest.skip(f"GSettings schema not available: {e}")


def test_play_skips_visual_when_disabled(monkeypatch, settings):
    c = StateInductionController(settings)
    # Ensure visual disabled
    c._settings.enable_visual_stimuli = False
    called = {"audio": 0, "visual": 0}
    def aplay():
        called["audio"] += 1
    def vplay():
        called["visual"] += 1
    c.audio_stimulus.play = aplay
    c.visual_stimulus.play = vplay
    c.play()
    assert called["audio"] == 1
    assert called["visual"] == 0


def test_play_runs_visual_when_enabled(monkeypatch, settings):
    c = StateInductionController(settings)
    c._settings.enable_visual_stimuli = True
    called = {"audio": 0, "visual": 0}
    c.audio_stimulus.play = lambda: called.__setitem__("audio", called["audio"] + 1)
    c.visual_stimulus.play = lambda: called.__setitem__("visual", called["visual"] + 1)
    c.play()
    assert called["audio"] == 1
    assert called["visual"] == 1


def test_pause_and_stop_call_children(monkeypatch, settings):
    c = StateInductionController(settings)
    c._settings.enable_visual_stimuli = True
    flags = {"ap": 0, "vp": 0, "as": 0, "vs": 0}
    c.audio_stimulus.pause = lambda: flags.__setitem__("ap", 1)
    c.visual_stimulus.pause = lambda: flags.__setitem__("vp", 1)
    c.audio_stimulus.stop = lambda: flags.__setitem__("as", 1)
    c.visual_stimulus.stop = lambda: flags.__setitem__("vs", 1)
    c.play()
    c.pause()
    assert flags["ap"] == 1 and flags["vp"] == 1
    c.stop()
    assert flags["as"] == 1 and flags["vs"] == 1
