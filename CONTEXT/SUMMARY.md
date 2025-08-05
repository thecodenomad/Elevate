# Project Summary

Elevate is a desktop application for inducing mental states (e.g., Sleep, Focus) through audio (binaural beats) and visual stimuli. It targets Linux users with a modern, adaptive GNOME interface using GTK4 and Libadwaita. Key features include state induction controls, customizable audio/visual stimuli, user settings, and an epilepsy warning dialog. The app is packaged as a Flatpak for distribution.

The application is built with Python 3.12, GTK4 4.12, Libadwaita 1.6, and uses Poetry for dependency management. It follows the GNOME Builder Python project template and is designed to be mobile-friendly with a sidebar for controls and a GL-based rendering area for visual stimuli.

## Core Components

- **AudioStimulus**: Generates binaural beats using GStreamer with configurable base frequency and channel offset
- **VisualStimulus**: Renders visual stimuli (colors, breathing patterns) using Cairo graphics
- **StateInductionController**: Coordinates audio and visual stimuli playback, managing the overall induction workflow
- **ElevateSettings**: Manages user preferences using GSettings for persistent configuration
- **UI Components**: Built with Blueprint templates and GTK4/Libadwaita widgets for a modern, responsive interface

## Key Features

- Adaptive UI with collapsible sidebar that works on both desktop and mobile
- Real-time audio generation with GStreamer for glitch-free playback
- Visual stimulus rendering with animated color transitions and breathing patterns
- Persistent settings management through GSettings
- Safety features including epilepsy warning dialogs
- Comprehensive test suite with 90%+ coverage for backend logic
- Flatpak packaging for easy distribution and installation

## Development Workflow

The project uses a modern development workflow with:
- Poetry for dependency management
- Meson for building and resource compilation
- Foundry for development tooling
- pytest for testing with coverage reports
- pylint and black for code quality and formatting
- GitHub Actions for continuous integration