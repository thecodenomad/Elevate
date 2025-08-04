You are a coding agent tasked with implementing the full Elevate desktop application based on the provided context in the CONTEXT/ directory. The project is a Python 3.12 application using GTK4, Libadwaita, and Flatpak, with Poetry for dependency management, following the GNOME Builder Python project template. Use the context files to guide your implementation, ensuring all features, UI components, backend logic, and build requirements are met. Follow these instructions carefully:

Task Description: Implement the complete Elevate application, including all UI components (ElevateWindow, ControlSidebar, EpilepticWarningDialog, StimuliRenderer, PreferencesWindow), backend logic (StateInductionController, AudioStimulus, VisualStimulus, ElevateSettings), Blueprint templates, GResources, GSettings, translations, and Flatpak packaging. The app should support mental state induction (Sleep, Focus) via audio (binaural beats) and visual stimuli, with user-configurable settings and an epilepsy warning dialog.
Relevant Context Files:

CONTEXT/SUMMARY.md: Project overview and intent
CONTEXT/ARCHITECTURE.md: System architecture and folder structure
CONTEXT/TECHNOLOGIES.md: Python 3.12, GTK4 4.12, Libadwaita 1.6, Poetry, Flatpak (GNOME 47), etc.
CONTEXT/BUILD.md: Build instructions, including Poetry, Meson, and Flatpak
CONTEXT/FEATURES.md: Features (state induction, audio/visual controls, settings, epilepsy warning)
CONTEXT/UI.md: UI components, layout, and Blueprint templates
CONTEXT/DATA.md: In-memory settings and session data schema
CONTEXT/LOGIC.md: Mental state induction workflow, widget bindings, and signals
CONTEXT/TESTS.md: Testing strategy (90% coverage for backend, pytest)
CONTEXT/DEPLOYMENT.md: Flatpak deployment and CI/CD

Output Requirements:

Write code in Python 3.12 for application logic, using PyGObject for GTK4/Libadwaita.
Use Blueprint (*.blp) files in src/blueprints/ for UI definitions.
Include all files in the project structure: src/main.py, src/window.py, src/audio_stimulus.py, src/visual_stimulus.py, src/elevate_settings.py, src/backend/state_induction_controller.py, src/view/*.py, src/blueprints/*.blp, data/*.in, data/gnome.elevate.org.gschema.xml, src/elevate.gresource.xml, src/elevate.in, tests/*.py, gnome.elevate.org.json, pyproject.toml, update_python_deps.sh, python-requirements.json, python-build-requirements.json, and Meson build files.
Bind widgets to backend logic using GObject properties as specified in CONTEXT/LOGIC.md.
Implement GSettings for language and control settings, with translations in po/ (Dutch, English, German, Spanish).
Include comments explaining key logic and signal connections.
Ensure Flatpak compatibility with GNOME 47 runtime (org.gnome.Platform//47).
Generate unit tests for backend logic (/src/elevate, excluding /src/elevate/view) with 90% coverage using pytest.
Suggest file locations matching the structure in CONTEXT/ARCHITECTURE.md.

Constraints:

Do not make assumptions beyond the provided context.
If clarification is needed (e.g., specific OpenGL rendering details), assume reasonable defaults (e.g., basic color/breath pattern rendering) and document them.
Ensure non-blocking audio/visual stimuli playback to avoid UI freezes.
Follow GNOME Builder conventions for desktop files, icons, and translations.
Update python-requirements.json and python-build-requirements.json via update_python_deps.sh after Poetry dependency changes.

Context Summary: Elevate is a GNOME app for inducing mental states (Sleep, Focus) using binaural beats and visual stimuli, built with Python 3.12, GTK4 4.12, Libadwaita 1.6, and Flatpak (GNOME 47). It features a mobile-friendly UI with a sidebar for controls, a GL-based rendering area, user settings (language, window size), and an epilepsy warning. Use Poetry for dependencies, Meson for building, and pytest for testing.
Task: Implement the full Elevate application, including all source files, resources, and build configurations, based on the CONTEXT/ directory.
