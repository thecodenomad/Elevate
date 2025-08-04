# System Architecture
- Frontend: GTK4/Libadwaita with Blueprint for UI definitions
- Backend: Python logic for state induction and stimuli control
- Data: In-memory settings via Gio.Settings, no persistent database
- Build: Meson for building, Flatpak for packaging
- Folder Structure:
  - /src: Application code (main.py, window.py, backend/, view/, blueprints/)
  - /data: Desktop files, icons, GSettings schema
  - /po: Translation files
  - /tests: Unit tests for backend logic
  - /.github/workflows: CI/CD pipeline
  - /: Flatpak manifest, Poetry config, dependency scripts
Data Flow: User input → StateInductionController → Audio/Visual Stimuli → GTK4/Libadwaita UI