# Requirements:
- Must use hardware acceleration where possible to give the smoothest graphics.
- Must use GTK4 and Python
- Must be extensible so that new animations can easily be added
- src/view/stimuli_renderer.py's StimuliRenderer is the parent class that will hold the GLArea these animations play in

# Animations

Each animation should have 4 phases, each phase has its own duration. Abstractly, these will correlate to:

- Phase 1: Inhale
- Phase 2: Post Inhale hold
- Phase 3: Exhale
- Phase 4: Post Exhale hold

Each phase must define if it is active, and what animation it should render.
Each phase should be as efficient as possible in rendering.
Each Animation will have a default phase tuple that corresponds to (4,4,4,4) which will be set externally from user preferences in GSettings.
Each Animation will have a phase cue for what they should be doing. Phase Cues should be an abstraction since the cue itself could be a visual or auditory cue.
Each Animation should have the ability to turn on or off the phase cue.
Each visual phase cue will have a position, font, and size requirement that is used by the Animation's render functionality.
Each Audio phase cue will have to have access to the currently running GStreamer pipeline in case binaural audio is currently playing.

Phase cues:
- phase1cue: "Breath In" or "1.mp3"
- phase2cue: "Hold Breath" or "2.mp3"
- phase3cue: "Breath Out" or "3.mp3"
- phase4cue: "Hold Breath" or "4.mp3"

As an abstract animation class, the user MUST provide the phase durations, and the phase cues at a minimum. Subclasses may have additional requirements as described in the animations described in the Feature Animations section.

## Feature Animations

## BouncyBall Animation
File: src/backend/animations/bouncy_ball.py
Class: BouncyBallAnimation

This particular animation will take in 3 colors:
- breath_color: Color for inhale/exhale phases
- hold_color: Color for hold phases
- background: Background color
Additional parameters:
- pulse_factor: Float < 1.0 for pulsation effect
- fade_duration: Duration for color fading transitions

The animation uses a tuple of floats of length 4 that corresponds to the duration (in seconds) for each phase:
Ex. phase_durations = (4,4,4,4)

Summary:

For this animation, there will be a circle that grows to the max of the GLArea during phase 1 (Inhale), during phase 2 (Hold) the circle will visibly 'pulsate' where the (max_diameter * pulse_factor) <= diameter <= (max diameter), during phase 3 (Exhale) shrinks back down to 0, and then during phase 4 (Hold) pulsates from 0 <= diameter <= (max_diameter * pulse_factor) before continuing back on to phase 1.

The animation features smooth color transitions between phases with configurable fade durations.
