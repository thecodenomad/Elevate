import numpy as np
import pytest
from elevate.backend.audio_stimulus import AudioStimulus


def test_generate_audio_buffer_shapes(monkeypatch):
    a = AudioStimulus()
    a.base_frequency = 220.0
    a.channel_offset = 5.0
    buf = a._generate_audio_buffer(0.05)
    assert isinstance(buf, np.ndarray)
    assert buf.dtype == np.float32
    assert buf.ndim == 2 and buf.shape[1] == 2


def test_play_pause_stop_state_transitions(monkeypatch):
    a = AudioStimulus()
    # Replace pipeline creation to avoid real gst
    calls = {"create": 0, "play": 0, "pause": 0, "stop": 0}
    def fake_create():
        calls["create"] += 1
        class P:
            def set_state(self, _):
                pass
        a._pipeline = P()
    a._create_pipeline = fake_create
    a.play()
    a.pause()
    a.stop()
    assert calls["create"] == 1


def test_play_sets_frequencies(monkeypatch):
    a = AudioStimulus()
    class Src:
        def __init__(self):
            self.props = {}
        def set_property(self, k, v):
            self.props[k] = v
    a._source_left = Src()
    a._source_right = Src()
    a._base_frequency = 220.0
    a._channel_offset = 5.0
    class Pipe:
        def set_state(self, _):
            pass
    a._pipeline = Pipe()
    a.play()
    assert a._source_left.props["freq"] == 220.0
    assert a._source_right.props["freq"] == 225.0
