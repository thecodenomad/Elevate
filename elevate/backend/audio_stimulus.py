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

"""Audio stimulus generator for binaural beats.

This module provides the AudioStimulus class, which generates binaural beats
using GStreamer. Binaural beats are auditory illusions created when two
slightly different frequencies are played separately to each ear.

The class uses GObject properties to manage audio parameters and provides
methods to control playback of the audio stimulus.
"""

import numpy as np
import gi

gi.require_version("Gst", "1.0")
from gi.repository import GObject, Gst, GLib


class AudioStimulus(GObject.Object):
    """Audio stimulus generator for binaural beats.

    This class creates binaural beats by generating two sine waves with
    slightly different frequencies and playing them separately to each ear.
    The difference in frequencies creates the binaural beat effect which
    can be used for state induction.

    Attributes:
        base_frequency (float): The base frequency for the left ear (in Hz).
        channel_offset (float): The frequency offset for the right ear (in Hz).
        is_playing (bool): Whether the audio is currently playing.
        sample_rate (int): Audio sample rate in Hz.
        volume (float): Audio volume level (0.0 to 1.0).
    """

    __gtype_name__ = "AudioStimulus"

    def __init__(self):
        """Initialize the audio stimulus generator.

        Sets up default values for audio parameters and initializes the
        GStreamer framework. Default values create a 30 Hz base frequency
        with a 10 Hz offset, producing a 10 Hz binaural beat.
        """
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

    def _on_base_frequency_changed(self, _obj, _pspec):
        """Debug handler for base-frequency changes.

        Args:
            _obj: The object that changed (unused).
            _pspec: The property specification (unused).
        """
        print(f"AudioStimulus: base-frequency changed to {self._base_frequency} Hz")

    def _on_channel_offset_changed(self, _obj, _pspec):
        """Debug handler for channel-offset changes.

        Args:
            _obj: The object that changed (unused).
            _pspec: The property specification (unused).
        """
        print(f"AudioStimulus: channel-offset changed to {self._channel_offset} Hz")

    def _schedule_frequency_update(self):
        """Schedule a frequency update to avoid rapid pipeline changes.

        This method uses a timer to debounce frequency updates, preventing
        rapid changes from causing pipeline instability.
        """
        if self._update_timeout_id is not None:
            GLib.source_remove(self._update_timeout_id)
        self._update_timeout_id = GLib.timeout_add(100, self._apply_frequency_update)

    def _apply_frequency_update(self):
        """Apply pending frequency updates to the pipeline.

        This method applies any pending frequency changes to the GStreamer
        pipeline elements and restarts playback if it was active.

        Returns:
            bool: False to indicate this is a one-time callback that should
                  not be repeated.
        """
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
            print(
                f"Applied frequency update: Left {self._base_frequency} Hz, "
                f"Right {self._base_frequency + self._channel_offset} Hz"
            )
        except (TypeError, ValueError) as e:
            print(f"Error applying frequency update: {e}")
        except (RuntimeError, GLib.Error) as e:
            print(f"Pipeline error applying frequency update: {e}")
        self._pending_frequency_update = False
        self._update_timeout_id = None
        return False

    @GObject.Property(type=float, default=30.0)
    def base_frequency(self):
        """Get the base frequency for the binaural beat.

        The base frequency is played to the left ear, and the base frequency
        plus channel offset is played to the right ear.

        Returns:
            float: The base frequency in Hz.
        """
        return self._base_frequency

    @base_frequency.setter
    def base_frequency(self, value):
        """Set the base frequency for the binaural beat.

        Args:
            value (float): The new base frequency in Hz.
        """
        self._base_frequency = float(value)
        self._pending_frequency_update = True
        self._schedule_frequency_update()

    @GObject.Property(type=float, default=10.0)
    def channel_offset(self):
        """Get the frequency offset between channels.

        This offset is added to the base frequency to determine the
        frequency played to the right ear.

        Returns:
            float: The channel offset in Hz.
        """
        return self._channel_offset

    @channel_offset.setter
    def channel_offset(self, value):
        """Set the frequency offset between channels.

        Args:
            value (float): The new channel offset in Hz.
        """
        self._channel_offset = float(value)
        self._pending_frequency_update = True
        self._schedule_frequency_update()

    def _generate_audio_buffer(self, duration):
        """Generate a stereo audio buffer with binaural beats.

        Creates a numpy array containing sine waves for both channels
        with the specified frequency parameters.

        Args:
            duration (float): Duration of audio to generate in seconds.

        Returns:
            numpy.ndarray: Stereo audio buffer as a 2D array of floats.
        """
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
        """Create the GStreamer pipeline for audio playback.

        This method sets up the GStreamer elements required for playing
        binaural beats, including two tone generators (one for each channel),
        a mixer to combine them, and an audio sink to output the sound.

        Raises:
            RuntimeError: If any required GStreamer elements cannot be created.
        """
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
            raise RuntimeError("Failed to create GStreamer elements")

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
        except (RuntimeError, GLib.Error):
            pass

    def _on_enough_data(self, src):
        """Callback when GStreamer has enough data.

        This method is called when the GStreamer pipeline has sufficient
        data to process. Currently this is a no-op handler.

        Args:
            src: The source element that has enough data
        """
        # This is intentionally left empty as a placeholder for future implementation

    def play(self):
        """Start playing the binaural beat.

        Initializes the GStreamer pipeline if it doesn't exist and
        sets it to the PLAYING state. If the pipeline is already
        playing, this method has no effect.
        """
        if not self._is_playing:
            try:
                if not self._pipeline:
                    self._create_pipeline()
                left_freq = float(self._base_frequency)
                right_freq = float(self._base_frequency + self._channel_offset)

                print(
                    f"Play initiated...\n\tLeft Channel: {left_freq} Hz, Right Channel: {right_freq} Hz"
                )

                # Ensure frequencies are applied to pipeline elements
                if self._source_left and self._source_right:
                    try:
                        self._source_left.set_property("freq", left_freq)
                        self._source_right.set_property("freq", right_freq)
                    except (TypeError, ValueError) as e:
                        print(f"Error setting frequencies on play: {e}")
                    except (RuntimeError, GLib.Error) as e:
                        print(f"Pipeline error setting frequencies on play: {e}")
                self._pipeline.set_state(Gst.State.PLAYING)
                self._is_playing = True
            except (RuntimeError, GLib.Error) as e:
                print(f"Error starting audio stream: {e}")

    def pause(self):
        """Pause the binaural beat.

        Sets the GStreamer pipeline to the PAUSED state. The audio
        will stop playing but the pipeline will remain ready to resume.
        """
        if self._is_playing and self._pipeline:
            self._pipeline.set_state(Gst.State.PAUSED)
            self._is_playing = False

    def stop(self):
        """Stop the binaural beat.

        Sets the GStreamer pipeline to the NULL state and releases
        all resources. The pipeline must be reinitialized to play again.
        """
        if self._pipeline:
            self._pipeline.set_state(Gst.State.NULL)
            self._pipeline = None
        self._is_playing = False

    def set_volume(self, value: float):
        """Set the volume level for the audio.

        Args:
            value (float): The desired volume level (0.0 to 1.0).
                          Values outside this range will be clamped.
        """
        self._volume = max(0.0, min(1.0, float(value)))
        try:
            if self._volume_element:
                self._volume_element.set_property("volume", float(self._volume))
        except (TypeError, ValueError) as e:
            print(f"Error setting volume {value}: {e}")
        except (RuntimeError, GLib.Error) as e:
            print(f"Pipeline error setting volume {value}: {e}")

    def get_volume(self) -> float:
        """Get the current volume level.

        Returns:
            float: The current volume level (0.0 to 1.0).
        """
        return float(self._volume)
