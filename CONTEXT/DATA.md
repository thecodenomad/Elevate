# Data Context
- Data Store: In-memory settings via Gio.Settings (data/org.thecodenomad.elevate.gschema.xml)
- Schema:
  - Settings: { base_frequency: double, channel_offset: double, enable_visual_stimuli: boolean, stimuli_type: int }
- No persistent database or external APIs

The GSettings schema defines the following keys:
- default_state (string): The intended brainwave state Delta, Theta, Beta, and Gamma (default: Delta)
- base-frequency (double): Base frequency for audio stimuli (default: 200.0)
- channel-offset (double): Channel offset for audio stimuli (default: 10.0)
- enable-visual-stimuli (boolean): Whether to enable visual stimuli (default: false)
- stimuli-type (int): Type of visual stimuli to use (default: 0)

These settings are automatically persisted by the GSettings system and loaded on application startup.
