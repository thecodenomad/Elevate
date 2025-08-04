# Logic Context
- Mental State Induction Workflow:
  1. User selects state outcome ("Sleep" → Delta, 0.5–4 Hz; "Focus" → Theta, 5–13 Hz)
  2. Configure audio (base frequency 100–300 Hz, channel offset 1–20 Hz) and visual stimuli (type, breath pattern)
  3. Start induction via play button
  4. Pause/stop induction as needed
- Widget Bindings:
  - Gtk.Scale (Base Frequency) → StateInductionController.base_frequency
  - Gtk.Scale (Channel Offset) → StateInductionController.channel_offset
  - Gtk.ComboRow (Stimuli Type) → StateInductionController.stimuli_type
  - Gtk.ComboRow (Breath Pattern) → StateInductionController.breath_pattern
  - Gtk.Entry (Breath In/Out/Hold) → StateInductionController.breath_*_interval
  - Gtk.ToggleButton (Show EEG/Record Session) → StateInductionController.show_eeg/record_session
- Signals:
  - Expand Icon (Gtk.Button): "toggled" → ElevateWindow.on_fullscreen_toggled
  - Play/Pause/Stop Buttons: "clicked" → StateInductionController.start/pause/stop_induction
  - Visual Stimuli Switch: "notify::active" → ControlSidebar.on_visual_stimuli_toggled
  - Settings Button: "clicked" → PreferencesWindow.present
- Error Handling:
  - Visual Stimuli Switch: Show EpilepticWarningDialog on enable
  - Invalid inputs: Disable play button for invalid frequencies/offsets