"""Extended tests for AudioStimulus covering buffer generation, volume handling, and frequency scheduling."""

import builtins
import numpy as np
import pytest
from unittest.mock import MagicMock, patch

# Import the class after patching gi imports to avoid actual GStreamer dependencies
with patch.dict('sys.modules', {
    'gi': MagicMock(),
    'gi.repository': MagicMock(),
}):
    from elevate.backend.audio_stimulus import AudioStimulus


def test_generate_audio_buffer_basic_shape_and_frequencies():
    """Verify that the generated audio buffer has correct shape and frequency content.

    The buffer should be a NumPy array of shape (N, 2) where N is the number of samples.
    The left channel should be a sine wave at ``base_frequency`` and the right channel
    at ``base_frequency + channel_offset``.
    """
    stim = AudioStimulus()
    # Use a short duration for quick test
    duration = 0.01  # seconds
    # Set known frequencies
    stim._base_frequency = 100.0
    stim._channel_offset = 20.0
    buffer = stim._generate_audio_buffer(duration)

    # Expected number of samples
    expected_samples = int(stim._sample_rate * duration)
    assert buffer.shape == (expected_samples, 2)
    # Verify dtype is float32
    assert buffer.dtype == np.float32

    # Check first few samples against analytical sine values
    t = np.arange(expected_samples) / stim._sample_rate
    left_expected = np.sin(2 * np.pi * stim._base_frequency * t)
    right_expected = np.sin(2 * np.pi * (stim._base_frequency + stim._channel_offset) * t)
    # Use a tolerance because of floating point rounding
    np.testing.assert_allclose(buffer[:, 0], left_expected, rtol=1e-5, atol=1e-7)
    np.testing.assert_allclose(buffer[:, 1], right_expected, rtol=1e-5, atol=1e-7)


def test_set_volume_clamps_and_updates_element(monkeypatch):
    """Test that ``set_volume`` clamps values between 0 and 1 and updates the GStreamer element.

    The method should store the clamped value and, if a volume element exists, call its
    ``set_property`` method with the new volume.
    """
    stim = AudioStimulus()
    # Create a mock volume element and assign it
    mock_volume_elem = MagicMock()
    stim._volume_element = mock_volume_elem

    # Test clamping below 0
    stim.set_volume(-0.5)
    assert stim.get_volume() == 0.0
    mock_volume_elem.set_property.assert_called_with('volume', 0.0)
    mock_volume_elem.set_property.reset_mock()

    # Test clamping above 1
    stim.set_volume(2.0)
    assert stim.get_volume() == 1.0
    mock_volume_elem.set_property.assert_called_with('volume', 1.0)
    mock_volume_elem.set_property.reset_mock()

    # Test a normal value within range
    stim.set_volume(0.42)
    assert pytest.approx(stim.get_volume(), rel=1e-6) == 0.42
    mock_volume_elem.set_property.assert_called_with('volume', 0.42)


def test_frequency_update_scheduling_and_application(monkeypatch):
    """Test that setting ``base_frequency`` or ``channel_offset`` schedules an update.

    The ``_schedule_frequency_update`` method should call ``GLib.timeout_add`` and
    store the timeout ID. The ``_apply_frequency_update`` method should apply the
    pending frequencies to the mocked source elements when called.
    """
    # Mock GLib functions
    timeout_ids = []
    def fake_timeout_add(interval, callback):
        timeout_ids.append((interval, callback))
        return 999  # dummy timeout id
    monkeypatch.setattr('gi.repository.GLib.timeout_add', fake_timeout_add)
    monkeypatch.setattr('gi.repository.GLib.source_remove', lambda src: None)

    stim = AudioStimulus()
    # Replace pipeline elements with mocks
    stim._source_left = MagicMock()
    stim._source_right = MagicMock()
    stim._pipeline = MagicMock()
    # Ensure pending flag is initially False
    assert not stim._pending_frequency_update

    # Change base frequency – should set pending flag and schedule timeout
    stim.base_frequency = 150.0
    assert stim._pending_frequency_update
    assert stim._update_timeout_id == 999
    assert timeout_ids, "GLib.timeout_add was not called"

    # Change channel offset – should also schedule (overwrites previous timeout)
    stim.channel_offset = 30.0
    assert stim._pending_frequency_update
    assert stim._update_timeout_id == 999

    # Simulate the timeout callback execution
    # The stored callback is the last element in timeout_ids
    _, callback = timeout_ids[-1]
    # Ensure the pipeline is in a playing state for the test
    stim._is_playing = True
    # Call the callback directly – it should apply frequencies and clear flags
    result = callback()
    # The callback should return False to stop further timeouts
    assert result is False
    # Verify that source elements received the correct frequencies
    stim._source_left.set_property.assert_called_with('freq', 150.0)
    stim._source_right.set_property.assert_called_with('freq', 180.0)  # 150 + 30
    # Pending flag should be cleared after applying
    assert not stim._pending_frequency_update
    # Timeout ID should be cleared
    assert stim._update_timeout_id is None
