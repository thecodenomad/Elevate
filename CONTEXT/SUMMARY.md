# Project Summary

Elevate is a desktop application for inducing mental states (e.g., Sleep, Focus) through audio (binaural beats) and visual stimuli. It targets Linux users with a modern, adaptive GNOME interface using GTK4 and Libadwaita. Key features include state induction controls, customizable audio/visual stimuli, user settings, and an epilepsy warning dialog. The app is packaged as a Flatpak for distribution.

The application is built with Python 3.12, GTK4 4.12, Libadwaita 1.6, and uses Poetry for dependency management. It follows the GNOME Builder Python project template and is designed to be mobile-friendly with a sidebar for controls and a DrawingArea for visual stimuli.

Updates:
- Audio engine uses GStreamer: two audiotestsrc (left/right) mixed via audiomixer → audioconvert → autoaudiosink. Left frequency = base; Right = base + offset. Properties update live during playback.
- UI bindings in window.py connect SpinRows/Switch/ComboRow to settings; DrawingArea renders via VisualStimulus.
- Tests use in-memory GSettings mock and Gst stub; UI excluded from coverage.
