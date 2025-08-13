# conftest.py
#
# Copyright 2025 thecodenomad
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# SPDX-License-Identifier: GPL-3.0-or-later

import os
import builtins
import types
import sys
import pytest

import elevate.settings as elevate_settings


@pytest.fixture(autouse=True, scope="session")
def mock_gsettings_for_tests():
    os.environ.setdefault("ELEVATE_TEST_MEMORY_SETTINGS", "1")

    class _MemorySettings:
        def __init__(self):
            self._values = {
                "base-frequency": 30.0,
                "channel-offset": 6.0,
                "intended-state": 0,
                "session-length": 10,
                "epileptic-warning": True,
                "language": 0,
                "enable-visual-stimuli": True,
                "saved-volume": 25,
                "stimuli-type": 1,
            }
            self._callbacks = {}

        def get_double(self, key):
            return float(self._values[key])

        def set_double(self, key, value):
            self._values[key] = float(value)
            self._emit_changed(key)

        def get_boolean(self, key):
            return bool(self._values[key])

        def set_boolean(self, key, value):
            self._values[key] = bool(value)
            self._emit_changed(key)

        def get_int(self, key):
            return int(self._values[key])

        def set_int(self, key, value):
            self._values[key] = int(value)
            self._emit_changed(key)

        def bind(self, source_prop, target, target_prop, flags):
            val = self._values.get(source_prop)
            if isinstance(val, float):
                target.set_property(target_prop, float(val))
            elif isinstance(val, bool):
                target.set_property(target_prop, bool(val))
            else:
                target.set_property(target_prop, int(val))

        def connect(self, signal, callback):
            if signal.startswith("changed::"):
                key = signal[len("changed::"):]
                self._callbacks[key] = callback

        def _emit_changed(self, key):
            callback = self._callbacks.get(key)
            if callback:
                callback(self, key)

    orig_init = elevate_settings.ElevateSettings.__init__

    def _patched_init(self):
        builtins.super(elevate_settings.ElevateSettings, self).__init__()
        self.app_config = _MemorySettings()

    elevate_settings.ElevateSettings.__init__ = _patched_init

    yield

    elevate_settings.ElevateSettings.__init__ = orig_init


@pytest.fixture(autouse=True)
def stub_gst(monkeypatch):
    class _DummyState:
        NULL = object()
        PLAYING = object()
        PAUSED = object()

    class _DummyBuffer:
        def __init__(self, size):
            self._size = size
            self.pts = None
            self.duration = None
        @classmethod
        def new_allocate(cls, *args):
            return cls(args[1])
        def fill(self, *args):
            return 0

    class _DummyCaps:
        @classmethod
        def from_string(cls, s):
            return ("caps", s)

    class _DummyElement:
        def __init__(self, name):
            self._name = name
            self._props = {}
            self._callbacks = {}
        def set_property(self, k, v):
            self._props[k] = v
        def get_property(self, k):
            return self._props.get(k)
        def link(self, other):
            return True
        def connect(self, sig, cb):
            self._callbacks[sig] = cb
        def emit(self, sig, *args):
            cb = self._callbacks.get(sig)
            if cb:
                return cb(self, *args)

    class _DummyPipeline(_DummyElement):
        def __init__(self, name):
            super().__init__(name)
            self._children = []
            self._state = _DummyState.NULL
        def add(self, elem):
            self._children.append(elem)
        def set_state(self, state):
            self._state = state

    class _DummyElementFactory:
        @staticmethod
        def make(kind, name):
            return _DummyElement(name)

    class DummyGst:
        State = _DummyState
        Buffer = _DummyBuffer
        Caps = _DummyCaps
        ElementFactory = _DummyElementFactory
        Pipeline = _DummyPipeline
        CLOCK_TIME_NONE = object()
        @staticmethod
        def init(_):
            return None

    # Only stub if gi Gst cannot be imported or tests request
    try:
        import gi  # noqa: F401
        from gi.repository import Gst as _real_gst  # type: ignore
        use_stub = False
    except Exception:
        use_stub = True

    if use_stub:
        sys.modules.setdefault("Gst", DummyGst)
        # Patch import site in audio_stimulus to use our DummyGst
        monkeypatch.setitem(sys.modules, "gi.repository.Gst", DummyGst)

    yield
