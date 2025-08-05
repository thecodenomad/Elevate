# Deployment
- Platform: Flatpak
- Runtime: org.gnome.Platform//47
- SDK: org.gnome.Sdk
- Env Vars: None
- Deployment: `foundry export`
- Distribution: Flathub (optional)
- CI/CD: GitHub Actions in .github/workflows/build.yml

The Flatpak manifest (org.thecodenomad.elevate.json) includes:
- GNOME 47 runtime dependencies
- Python dependencies via python-deps.json and python-build-deps.json
- Cleanup rules to remove development dependencies from the final package
- Bluetooth permissions for future EEG integration

Dependencies are managed through:
- Poetry for Python package management
- update_python_dependencies.sh script to generate Flatpak dependency files
- Meson for building and installing application files
