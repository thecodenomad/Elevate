import pytest
from elevate.backend.state_induction_controller import StateInductionController


def test_play_skips_visual_when_disabled(monkeypatch):
    c = StateInductionController()
    # Ensure visual disabled
    c._settings.set_enable_visual_stimuli(False)
    called = {"audio": 0, "visual": 0}
    def aplay():
        called["audio"] += 1
    def vplay():
        called["visual"] += 1
    c._audio_stimulus.play = aplay
    c._visual_stimulus.play = vplay
    c.play()
    assert called["audio"] == 1
    assert called["visual"] == 0


def test_play_runs_visual_when_enabled(monkeypatch):
    c = StateInductionController()
    c._settings.set_enable_visual_stimuli(True)
    called = {"audio": 0, "visual": 0}
    c._audio_stimulus.play = lambda: called.__setitem__("audio", called["audio"] + 1)
    c._visual_stimulus.play = lambda: called.__setitem__("visual", called["visual"] + 1)
    c.play()
    assert called["audio"] == 1
    assert called["visual"] == 1


def test_pause_and_stop_call_children(monkeypatch):
    c = StateInductionController()
    c._settings.set_enable_visual_stimuli(True)
    flags = {"ap": 0, "vp": 0, "as": 0, "vs": 0}
    c._audio_stimulus.pause = lambda: flags.__setitem__("ap", 1)
    c._visual_stimulus.pause = lambda: flags.__setitem__("vp", 1)
    c._audio_stimulus.stop = lambda: flags.__setitem__("as", 1)
    c._visual_stimulus.stop = lambda: flags.__setitem__("vs", 1)
    c.play()
    c.pause()
    assert flags["ap"] == 1 and flags["vp"] == 1
    c.stop()
    assert flags["as"] == 1 and flags["vs"] == 1
