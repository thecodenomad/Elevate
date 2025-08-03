# Project Structure

Backend Source: ./src
Custom UI Widgets: ./src/view
Blueprint Templates: ./src/blueprints
Tests: ./tests
Github Workflows: ./.github/workflows

# Main UI Components
The UI leverages GTK4 and libadwaita for a modern, adaptive design.

## 1. Main Window

Class: ElevateWindow
Inherits: Adw.ApplicationWindow
Location: src/window.py
Description: The primary window with a mobile-capable Adw.NavigationSplitView and a header bar.

Methods:

__init__: Initializes the window, sets up the header bar, and configures the split view.
on_fullscreen_toggled: Toggles full-screen mode when the expand icon is clicked.
on_play_clicked: Triggers the start of the sleep induction process.
on_pause_clicked: Pauses the sleep induction process.
on_stop_clicked: Stops the sleep induction process.


Signals:

"toggled" on the expand icon button to call on_fullscreen_toggled.
"clicked" on the play button to call on_play_clicked.
"clicked" on the pause button to call on_pause_clicked.
"clicked" on the stop button to call on_stop_clicked.

UI Elements:

Adw.HeaderBar: Contains sidebar button the left, a play pause and stop buttons in the center, and a expand icon settings button and close button on the right.
Adw.OverlaySplitView: to implement a utility pane where the sidebar can be hidden or shown
Expand Icon (Gtk.Button): Toggles full-screen mode.

The sidebar content of the Adw.OverlaySplitView should be a Adw.StatusPage which is defined by the "Control Sidebar"
The main content needs to be an Gtk.GLArea which is defined by the "Main Content Area"

## 2. Control Sidebar

Class: ControlSidebar
Inherits: Adw.StatusPage
Location: src/view/control_sidebar.py
Description: Sidebar revealed by the 'sidebar button', offering audio and visual stimuli controls.

Methods:

__init__: Sets up frequency, offset, and visual stimuli controls.
on_visual_stimuli_toggled: Shows the EpilepticWarningDialog if visual stimuli are enabled.
on_frequency_changed: Updates the base frequency value.
on_offset_changed: Updates the channel offset value.
on_stimuli_selected: Updates the selected visual stimuli type.

Signals:

"notify::active" on the visual stimuli switch to call on_visual_stimuli_toggled.
"value-changed" on the frequency Gtk.Scale to call on_frequency_changed.
"value-changed" on the offset Gtk.Scale to call on_offset_changed.
"notify::selected-item" on the Gtk.ComboRow to call on_stimuli_selected.

UI Elements:

There should be 4 preference groups in this sidebar, one to handle the intended BrainWave states, one to handle the Audio Stimuli, one to handle the Visual Stimuli, and one to handle advanced controls.

Adw.PreferencesGroup (Induce State) that is vertically oriented with horizontal expansion:
Gtk.ComboRow (State Outcome): Select Outcome (e.g. "Sleep", "Focus")
Adw.ExpanderRow (Advanced State Controls): Advanced options that exposes two more rows:
  Gtk.ComboRow (Brainwave State): Select Brainwave State (e.g. "Delta", "Theta", "Gamma")
  Gtk.SpinRow (Target Frequency): Set the target frequency (Hz) for BrainWaves, increments and decrements by .1

Adw.PreferencesGroup (Audio Stimuli) that is vertically oriented with horizontal expansion:
Gtk.Label: Label with "Base Frequency" set
Gtk.Scale (Base Frequency): Slider for setting base frequency (e.g., 100–300 Hz)
Gtk.Label: Label with "Channel Offset" set
Gtk.Scale (Channel Offset): Slider for setting channel offset (e.g., 1–20 Hz)

Adw.PreferencesGroup (Visual Stimuli):
Gtk.Switch (Visual Stimuli Enabled): Enables/disables visual stimuli.
Gtk.ComboRow (Visual Stimuli Type): Selects stimuli type (e.g., "Color", "Breath Pattern").
Gtk.ComboRow (Breath Pattern): Selects breath pattern type (e.g. "4-7-8", "Box")
Gtk.Box with styles "linked" and halign set to center. In this box should be 4 Gtk.Entry widgets "Breath In", "Hold", "Breath Out", "Hold" that is only visible when "Breath Pattern" is selected.

Adw.PreferenceGroup (Advanced):
Gtk.ToggleButton (Show EEG): Show EEG Feedback
Gtk.ToggleButton (Record Session): Record Session

The Induce State should have the logic that:
  When outcome is "Sleep", the Induction State is set to "Delta", and the target frequency ajustment is set to ".5-4Hz"
  When outcome is "Focus", the Induction State is set to "Theta", and the target frequency adjustment is set to "5-13Hz"

The Audio Stimuli Preference group should have a vertical orientation that expands horizontally with a title of "Audio Stimuli". The Audio Stimuli Preference group should also have a label "Base Frequency" above a Gtk.Scale for the Base Frequency. Below that should be another Label "Channel Offset" above a Gtk.Scale for the Channel Offset.

The Visual Stimuli Preference group should have a vertical orientation that expands horizontally with a title of "Visual Stimuli". The Visual Stimuli Preference group should have a Label "

## 3. Epileptic Warning Dialog

Class: EpilepticWarningDialog
Inherits: Adw.MessageDialog
Location: src/view/epileptic_warning_dialog.py
Description: Warns users about epilepsy risks when enabling visual stimuli.

Methods:

__init__: Sets up the dialog with a message and "Accept"/"Cancel" buttons.

UI Elements:

Message: "Visual stimuli may trigger seizures in individuals with epilepsy. Proceed with caution."
Buttons: "I Acknowledge" and "Cancel".

## 4. Main Content Area

Class: StimuliRenderer
Location: src/view/stimuli_renderer.py
Inherits: Gtk.GLArea
Description: Renders visual stimuli using OpenGL for hardware acceleration.
Methods:

__init__: Initializes the OpenGL context.
on_render: Renders the selected visual stimuli (e.g., color or breath pattern).
set_stimuli_type: Sets the type of stimuli to render.
start_rendering: Starts the rendering process.
stop_rendering: Stops the rendering process.

Signals:

"render" to call on_render for OpenGL drawing.

## 5. Preferences

Class: PreferencesWindow
Location: src/view/preferences_window.py
Inherits: Adw.Window
Description: Handles users settings for selecting the default language supporting Dutch, English, German, Spanish.

Methods:
__init__: Initializes the gsettings context using Gio.Settings.new(APPLICATION_ID)
on_language_change: Sets the default language and changes the language the app presents in


# Backend Components
Located in ./src, these classes manage the mental state induction logic.

## 1. Application Controller

Class: StateInductionController
Location: src/backend/state_induction_controller.py
Description: Coordinates the state induction process.
Methods:

__init__: Initializes with default settings.
set_base_frequency: Sets the base frequency for binaural beats.
set_channel_offset: Sets the channel offset for binaural beats.
set_visual_stimuli: Enables/disables and sets the visual stimuli type.
start_induction: Starts the process.
pause_induction: Pauses the process.
stop_induction: Stops the process.

## 2. Audio Stimuli Control

Class: AudioStimulus
Location: src/audio_stimulus.py
Description: Reactively manages binaural beats playback without blocking the UI when set or changed
Methods:

set_parameters: Sets base frequency and offset.
start: Begins playback.
stop: Stops playback.

## 3. Visual Stimuli Control

Class: VisualStimulus
Location: src/visual_stimulus.py
Description: Reactivly manages visual stimuli rendering logic without blocking the UI when set or changed
Methods:

set_color: Sets the color for color-based stimuli.
set_breath_pattern: Configures breath pattern parameters.
start: Begins rendering.
stop: Stops rendering.

## 4. Settings
Class: ElevateSettings
Location: src/elevate_settings.py
Description: Saves the users language preferences, the width and height of the main window, and the last values set for all of the input elements in the Control Sidebar.


# Blueprint Templates
Stored in ./src/blueprints as YAML files for UI definition.

## 1. Main Window Blueprint

File: src/blueprints/main_window.blp
Description: Defines the highlevel layout for the application

## 2. Control Sidebar Blueprint

File: src/blueprints/control_sidebar.blp
Description: Defines the layout controls

## 3. Epileptic Warning Dialog Blueprint

File: src/blueprints/epileptic_warning_dialog.blp
Description: Defines the epileptic warning dialog message and buttons.

## 4. Main Content Blueprint
File: src/blueprints/main_content.blp
Description: Defines the main content showing visualizations

## 5. Preferences Window Blueprint
File: src/blueprints/preferences_window.blp
Description: Defines the user preferences for selecting language

# Widget Linking
Widgets are linked to backend logic using GObject properties and signals:

Gtk.Scale "Base Frequency" should bind to StateInductionController.base_frequency
Gtk.Scale "Channel Offset" should bind to StateInductionController.channel_offset

Gtk.ComboRow "Stimuli Type" should bind to StateInductionController.stimuli_type
Gtk.ComboRow "Breath Pattern" should bind to StateInductionController.breath_pattern
Gtk.Entry "Breath In" should bind to StateInductionController.breath_in_interval
Gtk.Entry "Breath In Hold" should bind to StateInductionController.breath_in_hold_interval
Gtk.Entry "Breath Out" should bind to StateInductionController.breath_out_interval
Gtk.Entry "Breath Out Hold" should bind to StateInductionController.breath_out_hold_interval

Gtk.ToggleButton (Show EEG) should bind to StateInductionController.show_eeg
Gtk.ToggleButton (Record Session) should bind to StateInductionController.record_session

Visual Stimuli Switch: Connect "notify::active" to ControlSidebar.on_visual_stimuli_toggled.
Play/Pause/Stop Buttons: Connect "clicked" to SleepInductionController methods.
settings button: Connect "click" to present the PreferencesWindow

# Testing
Tests should have 90% coverage for all backend code in ./src ignore writing tests for code in ./src/view

# Build
All files need to be added to the `elevate_sources` variable in the src/meson.build
to guarantee being built into the application.
