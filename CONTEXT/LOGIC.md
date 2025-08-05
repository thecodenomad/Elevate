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
  - Gtk.SpinRow (Base Frequency) → ElevateSettings.base_frequency
  - Gtk.SpinRow (Channel Offset) → ElevateSettings.channel_offset
  - Gtk.Switch (Enable Visual Stimuli) → ElevateSettings.enable_visual_stimuli
  - Gtk.ComboRow (Stimuli Type) → ElevateSettings.stimuli_type
- Signals:
  - Play/Pause ToggleButton: "toggled" → ElevateWindow._on_play_toggled
  - Stop Button: "clicked" → ElevateWindow._on_stop_clicked
  - Sidebar Toggle Button: "clicked" → ElevateWindow._on_sidebar_toggle_clicked
  - Preferences Button: "clicked" → ElevateApplication.on_preferences_action
  - Controller "notify::is-playing": → ElevateWindow._on_playing_state_changed
- Error Handling:
  - Visual Stimuli Switch: Show EpilepticWarningDialog before enabling
  - GStreamer errors: Logged to console with user-friendly messages