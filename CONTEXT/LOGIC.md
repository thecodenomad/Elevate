# Logic Context
- Mental State Induction Workflow:
  1. User configures audio (base frequency 100–1000 Hz, channel offset 0.5–50 Hz) and visual stimuli (type)
  2. Start induction via play button
  3. Pause/stop induction as needed
- Component Interactions:
  - ElevateWindow ↔ StateInductionController: User actions trigger controller methods
  - StateInductionController ↔ AudioStimulus: Controller manages audio playback
  - StateInductionController ↔ VisualStimulus: Controller manages visual rendering
  - ElevateSettings ↔ All Components: Settings provide configuration values
- Widget Bindings:
  - Adw.SpinRow (Base Frequency adjustment.value) ↔ ElevateSettings.base-frequency
  - Adw.SpinRow (Channel Offset adjustment.value) ↔ ElevateSettings.channel-offset
  - Adw.SwitchRow.active ↔ ElevateSettings.enable-visual-stimuli
  - Adw.ComboRow.selected → ElevateSettings.stimuli-type
- Signals:
  - Play/Pause ToggleButton.toggled → ElevateWindow._on_play_toggled
  - Stop Button.clicked → ElevateWindow._on_stop_clicked
  - Sidebar Toggle Button.clicked → ElevateWindow._on_sidebar_toggle_clicked
  - Controller notify::is-playing → ElevateWindow._on_playing_state_changed
- Audio Engine:
  - GStreamer pipeline: audiotestsrc(left) + audiotestsrc(right) → audiomixer → audioconvert → autoaudiosink
  - Left freq = base_frequency; Right freq = base_frequency + channel_offset
  - Live updates: changing base_frequency or channel_offset while playing updates audiotestsrc freq props
- Testing:
  - tests/conftest.py provides in-memory GSettings mock and a Dummy Gst stub for headless testing
