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

import numpy as np
import gi

gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gst, GLib


class AudioStimulus(GObject.Object):
    """Audio stimulus generator for binaural beats."""

    __gtype_name__ = "AudioStimulus"

    def __init__(self):
        """Initialize the audio stimulus generator."""
        super().__init__()
        self._base_frequency = 30.0
        self._channel_offset = 10.0
        self._is_playing = False
        self._sample_rate = 44100
        self._buffer_size = 1024
        self._volume = 0.5
        self._pending_frequency_update = False  # Track pending updates
        self._update_timeout_id = None

        # Initialize GStreamer
        Gst.init(None)
        self._pipeline = None
        self._source_left = None
        self._source_right = None
        self._mixer = None
        self._audioconvert = None
        self._volume_element = None
        self._sink = None

        # Connect property change signals for debugging
        self.connect("notify::base-frequency", self._on_base_frequency_changed)
        self.connect("notify::channel-offset", self._on_channel_offset_changed)

    def _on_base_frequency_changed(self, obj, pspec):
        """Debug handler for base-frequency changes."""
        print(f"AudioStimulus: base-frequency changed to {self._base_frequency} Hz")

    def _on_channel_offset_changed(self, obj, pspec):
        """Debug handler for channel-offset changes."""
        print(f"AudioStimulus: channel-offset changed to {self._channel_offset} Hz")

    def _schedule_frequency_update(self):
        """Schedule a frequency update to avoid rapid pipeline changes."""
        if self._update_timeout_id is not None:
            GLib.source_remove(self._update_timeout_id)
        self._update_timeout_id = GLib.timeout_add(100, self._apply_frequency_update)

    def _apply_frequency_update(self):
        """Apply pending frequency updates to the pipeline."""
        if not self._pending_frequency_update or not self._source_left or not self._source_right:
            self._update_timeout_id = None
            return False
        was_playing = self._is_playing
        try:
            if was_playing:
                self._pipeline.set_state(Gst.State.PAUSED)
            self._source_left.set_property("freq", float(self._base_frequency))
            self._source_right.set_property("freq", float(self._base_frequency + self._channel_offset))
            if was_playing:
                self._pipeline.set_state(Gst.State.PLAYING)
            print(f"Applied frequency update: Left {self._base_frequency} Hz, Right {self._base_frequency + self._channel_offset} Hz")
        except TypeError as e:
            print(f"Error applying frequency update: {e}")
        except Exception as e:
            print(f"Unexpected error applying frequency update: {e}")
        self._pending_frequency_update = False
        self._update_timeout_id = None
        return False

    @GObject.Property(type=float, default=30.0)
    def base_frequency(self):
        """Get the base frequency for the binaural beat."""
        return self._base_frequency

    @base_frequency.setter
    def base_frequency(self, value):
        """Set the base frequency for the binaural beat."""
        self._base_frequency = float(value)
        self._pending_frequency_update = True
        self._schedule_frequency_update()

    @GObject.Property(type=float, default=10.0)
    def channel_offset(self):
        """Get the frequency offset between channels."""
        return self._channel_offset

    @channel_offset.setter
    def channel_offset(self, value):
        """Set the frequency offset between channels."""
        self._channel_offset = float(value)
        self._pending_frequency_update = True
        self._schedule_frequency_update()

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

        if not all(
            [
                self._pipeline,
                self._source_left,
                self._source_right,
                self._mixer,
                self._audioconvert,
                self._volume_element,
                self._sink,
            ]
        ):
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
            if src:
                src.set_property("wave", 0)
                src.set_property("volume", 1.0)
                src.set_property("is-live", True)
        if self._volume_element:
            self._volume_element.set_property("volume", float(self._volume))

        # Set initial frequencies
        if self._source_left and self._source_right:
            self._source_left.set_property("freq", float(self._base_frequency))
            self._source_right.set_property("freq", float(self._base_frequency + self._channel_offset))

        # Probe example hook (no-op handler)
        try:
            if self._source_left:
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

                print(f"Play initiated...Left: {left_freq} Hz, Right: {right_freq} Hz")

                # Ensure frequencies are applied to pipeline elements
                if self._source_left and self._source_right:
                    try:
                        self._source_left.set_property("freq", left_freq)
                        self._source_right.set_property("freq", right_freq)
                    except TypeError as e:
                        print(f"Error setting frequencies on play: {e}")
                    except Exception as e:
                        print(f"Unexpected error setting frequencies on play: {e}")
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
                print(f"Volume set to: {self._volume}")
        except TypeError as e:
            print(f"Error setting volume {value}: {e}")
        except Exception as e:
            print(f"Unexpected error setting volume {value}: {e}")

    def get_volume(self) -> float:
        return float(self._volume)
