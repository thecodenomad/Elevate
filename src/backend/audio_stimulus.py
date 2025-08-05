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
        
        # Initialize GStreamer
        Gst.init(None)
        self._pipeline = None
        self._source = None
        self._audioconvert = None
        self._audioresample = None
        self._sink = None

    @GObject.Property(type=float, default=200.0)
    def base_frequency(self):
        """Get the base frequency for the binaural beat."""
        return self._base_frequency

    @base_frequency.setter
    def base_frequency(self, value):
        """Set the base frequency for the binaural beat."""
        self._base_frequency = value

    @GObject.Property(type=float, default=10.0)
    def channel_offset(self):
        """Get the frequency offset between channels."""
        return self._channel_offset

    @channel_offset.setter
    def channel_offset(self, value):
        """Set the frequency offset between channels."""
        self._channel_offset = value

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
        """Create GStreamer pipeline for audio playback."""
        # Create pipeline
        self._pipeline = Gst.Pipeline.new("audio-pipeline")
        
        # Create elements
        self._source = Gst.ElementFactory.make("appsrc", "audio-source")
        self._audioconvert = Gst.ElementFactory.make("audioconvert", "audio-convert")
        self._audioresample = Gst.ElementFactory.make("audioresample", "audio-resample")
        self._sink = Gst.ElementFactory.make("autoaudiosink", "audio-sink")
        
        if not self._source or not self._audioconvert or not self._audioresample or not self._sink:
            raise Exception("Failed to create GStreamer elements")
        
        # Configure appsrc
        self._source.set_property("format", Gst.Format.TIME)
        self._source.set_property("is-live", True)
        self._source.set_property("do-timestamp", True)
        
        # Set caps for audio (stereo, float32, 44100 Hz)
        caps = Gst.Caps.from_string(
            f"audio/x-raw, format=F32LE, layout=interleaved, rate={self._sample_rate}, channels=2"
        )
        self._source.set_property("caps", caps)
        
        # Add elements to pipeline
        self._pipeline.add(self._source)
        self._pipeline.add(self._audioconvert)
        self._pipeline.add(self._audioresample)
        self._pipeline.add(self._sink)
        
        # Link elements
        self._source.link(self._audioconvert)
        self._audioconvert.link(self._audioresample)
        self._audioresample.link(self._sink)
        
        # Connect signal handlers
        self._source.connect("need-data", self._on_need_data)
        self._source.connect("enough-data", self._on_enough_data)

    def _on_need_data(self, src, length):
        """Callback when GStreamer needs more audio data."""
        # Generate 100ms of audio data
        duration = 0.1  # 100ms
        audio_data = self._generate_audio_buffer(duration)
        
        # Create buffer
        buffer = Gst.Buffer.new_allocate(None, len(audio_data.tobytes()), None)
        buffer.fill(0, audio_data.tobytes())
        buffer.pts = Gst.CLOCK_TIME_NONE
        buffer.duration = Gst.CLOCK_TIME_NONE
        
        # Push buffer to source
        src.emit("push-buffer", buffer)

    def _on_enough_data(self, src):
        """Callback when GStreamer has enough data."""
        pass

    def play(self):
        """Start playing the binaural beat."""
        if not self._is_playing:
            try:
                if not self._pipeline:
                    self._create_pipeline()
                
                # Set pipeline to playing state
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