# Deployment
- Platform: Flatpak
- Runtime: org.gnome.Platform//47
- SDK: org.gnome.Sdk//47
- Audio: Prefer PipeWire; add `--socket=pipewire` in finish-args. For fallback, consider `--socket=pulseaudio`.
- Env tips: In sandboxed/dev environments without audio, set `ALSOFT_DRIVERS=null` or `GST_AUDIO_SINK=fakesink` to avoid backend errors.
- Deployment: `foundry export`
- Distribution: Flathub (optional)
- CI/CD: GitHub Actions in .github/workflows/build.yml

The Flatpak manifest (org.thecodenomad.elevate.json) includes:
- GNOME 47 runtime
- Python dependencies via python-deps.json and python-build-deps.json
- Meson build system integration

Permissions:
- `--socket=pipewire`
- Optional: `--device=all` if needed for advanced audio backends (avoid unless required)
