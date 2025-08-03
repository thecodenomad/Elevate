# Project Structure

Backend Source: ./src
Custom UI Widgets: ./src/view
Blueprint Templates: ./src/view/blueprints
Tests: ./tests

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

Adw.HeaderBar: Contains play, pause, stop buttons, and an expand icon.
Adw.NavigationSplitView: Manages the sidebar (ControlSidebar) and content area (StimuliRenderer).
Expand Icon (Gtk.Button): Toggles full-screen mode.

## 2. Control Sidebar

Class: ControlSidebar
Inherits: Adw.PreferencesPage
Description: Sidebar revealed by the control menu, offering audio and visual stimuli controls.
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

Gtk.Scale (Base Frequency): Slider for setting base frequency (e.g., 100–300 Hz).
Gtk.Scale (Channel Offset): Slider for setting channel offset (e.g., 1–20 Hz).
Adw.PreferencesGroup (Visual Stimuli):

Gtk.Switch: Enables/disables visual stimuli.
Gtk.ComboRow: Selects stimuli type (e.g., "Color", "Breath Pattern").

## 3. Epileptic Warning Dialog

Class: EpilepticWarningDialog
Inherits: Adw.MessageDialog
Description: Warns users about epilepsy risks when enabling visual stimuli.
Methods:

__init__: Sets up the dialog with a message and "Accept"/"Cancel" buttons.

UI Elements:

Message: "Visual stimuli may trigger seizures in individuals with epilepsy. Proceed with caution."
Buttons: "Accept" and "Cancel".

## 4. Main Content Area

Class: StimuliRenderer
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

# Backend Components
Located in ./src, these classes manage the sleep induction logic.

## 1. Application Controller

Class: SleepInductionController
Description: Coordinates the sleep induction process.
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
Description: Manages binaural beats playback.
Methods:

set_parameters: Sets base frequency and offset.
start: Begins playback.
stop: Stops playback.

## 3. Visual Stimuli Control

Class: VisualStimulus
Description: Manages visual stimuli rendering logic.
Methods:

set_color: Sets the color for color-based stimuli.
set_breath_pattern: Configures breath pattern parameters.
start: Begins rendering.
stop: Stops rendering.

# Blueprint Templates
Stored in ./src/view/blueprints as YAML files for UI definition.

## 1. Main Window Blueprint

File: main_window.blp
Description: Defines the Adw.NavigationSplitView, header bar, and placeholders for sidebar and content.

## 2. Control Sidebar Blueprint

File: control_sidebar.blp
Description: Defines the layout for frequency, offset, and visual stimuli controls.

## 3. Epileptic Warning Dialog Blueprint

File: epileptic_warning_dialog.blp
Description: Defines the dialog’s message and buttons.

# Widget Linking
Widgets are linked to backend logic using GObject properties and signals:

Frequency Slider: Bind value to SleepInductionController.base_frequency.
Offset Slider: Bind value to SleepInductionController.channel_offset.
Visual Stimuli Switch: Connect "notify::active" to ControlSidebar.on_visual_stimuli_toggled.
ComboRow: Bind selected-item to VisualStimulus type via set_stimuli_type.
Play/Pause/Stop Buttons: Connect "clicked" to SleepInductionController methods.

# Testing
Tests should have at least 80% coverage for all backend code in ./src not UI elements in ./src/view
