# Data Context
- Data Store: In-memory settings via Gio.Settings (data/gnome.elevate.org.gschema.xml)
- Schema:
  - Settings: { language: string, window_width: int, window_height: int, base_frequency: float, channel_offset: float, stimuli_type: string, breath_pattern: string, breath_in_interval: float, breath_in_hold_interval: float, breath_out_interval: float, breath_out_hold_interval: float, show_eeg: bool, record_session: bool }
  - Session: { state_outcome: string, brainwave_state: string, target_frequency: float }
- No persistent database or external APIs