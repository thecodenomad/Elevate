# Requirements:
- Must use hardware accelereation where possible to give the smoothest graphics.
- Must use GTK4 and python
- Must be extensible so that new animations can easily be added
- src/stimuli_renderer.py's StimuliRenderer is the parent class that will hold the GLArea these animations play in

# Animations

Each animation should have 4 phases, each phase has it's own duration. Abtractly, these will correlate to:

phase1 - Inhale
phase2 - Post Inhale hold
phase3 - Exhale
phase4 - Post Exhale hold

Each phase must define if it is active, and what animation it should render.
Each phase should be as efficient as possible in rendering.
Each Animation will have a default phase tuple that corresponds to (4,4,4,4) which will be set externally from user preferences in GSettings.
Each Animation will have a phase cue for what they should be doing. Phase Cues should be an abstraction since the cue itself could be a visual or auditory cue.
Each Animation should have the ability to turn on or off the phase cue.
Each visual phase cue will have a position, font, and size requirement that is used by the Animation's render functionality.
Each Audio phase cue will have to have have access to the currently running GStreamer pipeline in case binaraul audio is currently playing.

phase1cue - "Breath In" or "1.mp3"
phase2cue - "Hold Breath" or "2.mp3"
phase3cue - "Breath Out" or "3.mp3"
phase4cue - "Hold Breath" or "4.mp3"

As an abstract animation class, the user MUST provide the phase durations, and the phase cues at a minimum. Subclasses may have additional requirements as described in the animations described in the Feature Animations section.

## Feature Animations

### Color Swap
File: src/backend/animation/color_swap.py
Class: ColorSwap

This particular animation will take in 4 colors corresponding one for each phase, a fade duration (float), and a tupel (float) of length 4 that corresponds to a duration (in seconds) for each phase:

Ex. phase_tuple = (4,4,4,4), phase_colors = (#FFFFFF, #EEEEEE, #DDDDDD, #CCCCCC)

On instantiation:

self._phase1duration, self._phase2duration, self._phase3duration, self._phase4duration = phase_tuple
self._phase1color, self._phase2color, self._phase3color, self._phase4color = phase_colors
self.fade_duation = fade_duration

Summary:

For this animation, each color will fill the GLArea for the phase duration and fade into the next color over the fade_ruation. For instance, with a fade_duration = .5 and self._phase1 = 4, the self._phase2color will start fading in at the 3.5 second mark and reach full opacity at the 4 second mark. If the user provided phase cues, then the animation will display or play the phase cue based on their specifications. The colors and cues should be easily swapped during runtime.

## BouncyBall Animation
File: src/backend/animation/bouncy_ball.py
Class: BouncyBall

This particular animation will take in 2 colors corresponding to the background and the fill of a single circle centered in the GLArea, a pulse_factor (float < 1.0), and a tuple (float) of length 4 that corresponds to the duration (in seconds) for each phase:

Ex. phase_tuple = (4,4,4,4), phase_colors = (#FFFFFF, #EEEEEE)

self._phase1duration, self._phase2duration, self._phase3duration, self._phase4duration = phase_tuple
self._phase1color, self._phase2color = phase_colors

Summary:

For this animation, there will be a circle that grows to the max of the GLArea during phase1duration, during phase2duration the circle will visably 'pulsate' where the (max_diameter* pulse_factor) <= diameter <= (max diameter), during phase3duration shrinks back down to 0, and then during phase4duration pulsates from 0 <= diameter <= (max_diameter - (max_diameter * pulse_factor)) before continuing back on to phase1duration. If the user provided phase cues, then the animation will display or play the phase cue based on their specifications. The colors and cues should be easily swapped during runtime.
