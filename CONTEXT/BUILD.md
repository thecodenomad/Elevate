# Build Instructions
- Install dependencies: `poetry install`
- Update Flatpak dependencies: `poetry update && ./update_python_dependencies.sh`
- Build: `foundry build`
- Run: `foundry run`
- Flatpak build: `foundry export`
- Lint: `poetry run pylint src/`
- Formatting: `poetry run black src/`
- Test: `poetry run pytest`

Notes:
- Audio in dev/CI: if no audio device, set `ALSOFT_DRIVERS=null` or `GST_AUDIO_SINK=fakesink` to avoid backend errors
- PipeWire recommended for Flatpak: ensure `--socket=pipewire` in manifest
- Coverage excludes UI paths; see pyproject.toml for pytest/coverage config
- Blueprint files (.blp) are compiled and bundled via Meson into GResources; window.blp ids must match window.py Gtk.Template.Child names
