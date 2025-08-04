# Build Instructions
- Install Poetry: `which poetry &> /dev/null || brew install poetry==2.1.3`
- Install dependencies: `poetry install`
- Update Flatpak dependencies: `poetry update && ./update_python_deps.sh`
- Add all source files to `elevate_sources` in `src/meson.build`
- Build: `foundry build`
- Run: `foundry run`
- Flatpak build: `foundry export`
- Lint: `poetry run pylint src/`
- Formatting: `poetry run black src/`
