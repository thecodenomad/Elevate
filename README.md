# Elevate

Elevate is a desktop application for inducing mental states (e.g., Sleep, Focus) through audio (binaural beats) and visual stimuli. It targets Linux users with a modern, adaptive GNOME interface using GTK4 and Libadwaita.

## Features

- Mental State Induction: Induce states like Sleep or Focus using scientifically-backed methods
- Audio Stimuli: Customize binaural beats with adjustable base frequency and channel offset
- Visual Stimuli: Enable visual effects like color pulses and breathing patterns
- Responsive UI: Adaptive layout that works on both desktop and mobile devices
- Safety First: Epilepsy warning dialog for visual stimuli

## Technologies

- Python 3.12
- GTK4 4.12 and Libadwaita 1.6
- GStreamer for audio processing
- Cairo for visual rendering
- Poetry for dependency management
- Meson for building
- Flatpak for packaging

## Installation

1. Install dependencies:
   ```
   poetry install
   ```

2. Run the application:
   ```
   poetry run python -m src.main
   ```

   Or using Foundry:
   ```
   foundry run
   ```

## Building

To build the application:
```
foundry build
```

To create a Flatpak package:
```
foundry export
```

## Development

To run tests:
```
poetry run pytest
```

To lint the code:
```
poetry run pylint src/
```

To format the code:
```
poetry run black src/
```

## License

This project is licensed under the GPL-3.0 License - see the LICENSE file for details.
