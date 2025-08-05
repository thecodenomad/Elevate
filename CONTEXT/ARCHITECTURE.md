# System Architecture
- Frontend: GTK4/Libadwaita with Blueprint for UI definitions
- Backend: Python logic for state induction and stimuli control
- Data: In-memory settings via Gio.Settings (GSettings), no persistent database
- Build: Meson for building, Foundry for development workflow, Flatpak for packaging
- Folder Structure:
  - /src: Application code (main.py, window.py, backend/, view/, blueprints/)
    - /src/backend: Core logic (audio_stimulus.py, visual_stimulus.py, state_induction_controller.py, elevate_settings.py)
    - /src/view: UI components (control_sidebar.py, epileptic_warning_dialog.py, preferences_window.py, stimuli_renderer.py)
    - /src/blueprints: UI definitions (*.blp)
  - /data: Desktop files, icons, GSettings schema
  - /po: Translation files
  - /tests: Unit tests for backend logic
  - /.github/workflows: CI/CD pipeline
  - /: Flatpak manifest, Poetry config, dependency scripts, Meson build files
Data Flow: User input → StateInductionController → Audio/Visual Stimuli → GTK4/Libadwaita UI