# audio_stimulus.py
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

"""Audio stimulus generator for binaural beats."""

import math
import numpy as np
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, GLib, Gst


class AudioStimulus(GObject.Object):
    """Audio stimulus generator for binaural beats."""

    __gtype_name__ = "AudioStimulus"

    def __init__(self):
        """Initialize the audio stimulus generator."""
        super().__init__()
        self._base_frequency = 200.0
        self._channel_offset = 10.0
        self._is_playing = False
        self._sample_rate = 44100
        self._buffer_size = 1024
        self._volume = 0.5
        
        # Initialize GStreamer
        Gst.init(None)
        self._pipeline = None
        self._source_left = None
        self._source_right = None
        self._mixer = None
        self._audioconvert = None
        self._volume_element = None
        self._sink = None

    @GObject.Property(type=float, default=200.0)
    def base_frequency(self):
        """Get the base frequency for the binaural beat."""
        return self._base_frequency

    @base_frequency.setter
    def base_frequency(self, value):
        self._base_frequency = value
        if self._is_playing and self._source_left and self._source_right:
            try:
                self._source_left.set_property("freq", float(self._base_frequency))
                self._source_right.set_property(
                    "freq", float(self._base_frequency + self._channel_offset)
                )
            except Exception:
                pass

    @GObject.Property(type=float, default=10.0)
    def channel_offset(self):
        """Get the frequency offset between channels."""
        return self._channel_offset

    @channel_offset.setter
    def channel_offset(self, value):
        self._channel_offset = value
        if self._is_playing and self._source_left and self._source_right:
            try:
                self._source_right.set_property(
                    "freq", float(self._base_frequency + self._channel_offset)
                )
            except Exception:
                pass

    def _generate_audio_buffer(self, duration):
        """Generate a stereo audio buffer with binaural beats."""
        # Calculate number of samples for the given duration
        num_samples = int(self._sample_rate * duration)
        
        # Generate time array
        t = np.arange(num_samples) / self._sample_rate

        # Generate left channel (base frequency)
        left_channel = np.sin(2 * np.pi * self._base_frequency * t)

        # Generate right channel (base frequency + offset)
        right_channel = np.sin(2 * np.pi * (self._base_frequency + self._channel_offset) * t)

        # Combine channels
        stereo_output = np.column_stack((left_channel, right_channel))
        
        return stereo_output.astype(np.float32)

    def _create_pipeline(self):
        self._pipeline = Gst.Pipeline.new("tone-player-pipeline")
        self._source_left = Gst.ElementFactory.make("audiotestsrc", "src_left")
        self._source_right = Gst.ElementFactory.make("audiotestsrc", "src_right")
        self._mixer = Gst.ElementFactory.make("audiomixer", "mixer")
        self._audioconvert = Gst.ElementFactory.make("audioconvert", "convert")
        self._volume_element = Gst.ElementFactory.make("volume", "volume")
        self._sink = Gst.ElementFactory.make("autoaudiosink", "audio-sink")

        if not all([self._pipeline, self._source_left, self._source_right, self._mixer, self._audioconvert, self._volume_element, self._sink]):
            raise Exception("Failed to create GStreamer elements")

        self._pipeline.add(self._source_left)
        self._pipeline.add(self._source_right)
        self._pipeline.add(self._mixer)
        self._pipeline.add(self._audioconvert)
        self._pipeline.add(self._volume_element)
        self._pipeline.add(self._sink)

        self._source_left.link_pads("src", self._mixer, "sink_0")
        self._source_right.link_pads("src", self._mixer, "sink_1")
        self._mixer.link(self._audioconvert)
        self._audioconvert.link(self._volume_element)
        self._volume_element.link(self._sink)

        # Configure defaults
        for src in (self._source_left, self._source_right):
            src.set_property("wave", 0)
            src.set_property("volume", 1.0)
            src.set_property("is-live", True)
        self._volume_element.set_property("volume", float(self._volume))

        # Probe example hook (no-op handler)
        try:
            pad = self._source_left.get_static_pad("src")
            pad.add_probe(Gst.PadProbeType.BUFFER, lambda *args: Gst.PadProbeReturn.OK, None)
        except Exception:
            pass


    def _on_enough_data(self, src):
        """Callback when GStreamer has enough data."""
        pass

    def play(self):
        if not self._is_playing:
            try:
                if not self._pipeline:
                    self._create_pipeline()
                left_freq = float(self._base_frequency)
                right_freq = float(self._base_frequency + self._channel_offset)
                self._source_left.set_property("freq", left_freq)
                self._source_right.set_property("freq", right_freq)
                self._pipeline.set_state(Gst.State.PLAYING)
                self._is_playing = True
            except Exception as e:
                print(f"Error starting audio stream: {e}")

    def pause(self):
        """Pause the binaural beat."""
        if self._is_playing and self._pipeline:
            self._pipeline.set_state(Gst.State.PAUSED)
            self._is_playing = False

    def stop(self):
        """Stop the binaural beat."""
        if self._pipeline:
            self._pipeline.set_state(Gst.State.NULL)
            self._pipeline = None
        self._is_playing = False

    def set_volume(self, value: float):
        self._volume = max(0.0, min(1.0, float(value)))
        try:
            if self._volume_element:
                self._volume_element.set_property("volume", float(self._volume))
        except Exception:
            pass

    def get_volume(self) -> float:
        return float(self._volume)