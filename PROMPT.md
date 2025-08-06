You are a coding agent tasked with implementing the full Elevate desktop application based on the provided context in the CONTEXT/ directory. Use the context files to guide your implementation, ensuring all features, UI components, backend logic, and build requirements are met.

Key requirements updated:
- Audio: Implement binaural beats with GStreamer pipeline using two audiotestsrc (left/right) → audiomixer → audioconvert → autoaudiosink. Left channel frequency = base_frequency; right channel = base_frequency + channel_offset. Update source frequencies live when properties change.
- UI: In window.blp, ensure IDs: sidebar_toggle_button, preferences_button, split_view, frequency_scale, channel_offset_scale, visual_stimuli_switch, stimuli_type_combo, stimuli_renderer, play_button, stop_button. In window.py, bind SpinRows/Switch to ElevateSettings properties, hook ComboRow.selected to stimuli-type, set DrawingArea draw func to VisualStimulus.render, and wire play/pause/stop.
- GTK versioning: In all modules importing Gtk, call gi.require_version('Gtk','4.0') before importing from gi.repository.
- Settings: Use Gio.Settings schema; tests should mock settings in-memory. Provide bind_property compatibility.
- Tests: Achieve ≥90% coverage for backend (exclude src/main.py, src/window.py, src/view/*). Provide Gst stub and GSettings mock in tests/conftest.py.
- Deployment: Prefer PipeWire in Flatpak (add --socket=pipewire). For dev/CI without audio, allow ALSOFT_DRIVERS=null or GST_AUDIO_SINK=fakesink.

Follow CONTEXT/* for architecture, features, logic, UI, build, tests, and deployment details. Ensure non-blocking audio/visual playback, GNOME conventions, and Meson/Flatpak integration.