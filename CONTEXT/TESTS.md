# Testing Strategy
- Framework: pytest 8.3
- Types: Unit tests for backend logic
- Coverage: 90% for /src/elevate (exclude /src/elevate/view)
- Test Cases:
  - Test StateInductionController: Initialization, frequency/offset settings, start/pause/stop
  - Test AudioStimulus: Parameter setting, playback start/stop
  - Test VisualStimulus: Color/breath pattern setting, rendering start/stop
  - Test ElevateSettings: Language and control settings persistence