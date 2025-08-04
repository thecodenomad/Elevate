# Build Instructions
- Install Poetry: `pip install poetry==1.8`
- Install dependencies: `poetry install`
- Update Flatpak dependencies: `poetry update && ./update_python_deps.sh`
- Install Flatpak runtimes: `flatpak install org.gnome.Sdk//47 org.gnome.Platform//47`
- Add all source files to `elevate_sources` in `src/meson.build`
- Build: `meson setup builddir && meson compile -C builddir`
- Run: `poetry run python -m elevate`
- Flatpak build: `flatpak-builder build gnome.elevate.org.json`