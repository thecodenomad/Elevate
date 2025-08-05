# Build Instructions
- Install dependencies: `poetry install`
- Update Flatpak dependencies: `poetry update && ./update_python_dependencies.sh`
- Build: `foundry build`
- Run: `foundry run`
- Flatpak build: `foundry export`
- Lint: `poetry run pylint src/`
- Formatting: `poetry run black src/`
- Test: `poetry run pytest`

The build process uses Meson for compiling resources and Python files. Blueprint files (.blp) are compiled to UI files, which are then bundled into a GResource file. The application is installed with proper directory structure preservation for Python modules.
