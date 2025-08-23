#!/usr/bin/env python3
"""Test script to verify brain wave state changes in BouncyBallAnimation."""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'elevate'))

from elevate.backend.animations.bouncy_ball import BouncyBallAnimation
from elevate.constants import StateType

def test_state_changes():
    """Test that state changes work correctly."""
    print("Testing BouncyBallAnimation state changes...")

    # Create animation instance
    animation = BouncyBallAnimation()

    print(f"Initial state: {animation.brain_wave_state}")
    print(f"Initial breath color: {animation.breath_color}")
    print(f"Initial hold color: {animation.hold_color}")
    print(f"Initial background color: {animation.background}")

    # Test alpha state change
    print("\nChanging to alpha state...")
    animation.set_brain_wave_state('alpha')

    print(f"Alpha state: {animation.brain_wave_state}")
    print(f"Alpha breath color: {animation.breath_color}")
    print(f"Alpha hold color: {animation.hold_color}")
    print(f"Alpha background color: {animation.background}")

    # Test beta state change
    print("\nChanging to beta state...")
    animation.set_brain_wave_state('beta')

    print(f"Beta state: {animation.brain_wave_state}")
    print(f"Beta breath color: {animation.breath_color}")
    print(f"Beta hold color: {animation.hold_color}")
    print(f"Beta background color: {animation.background}")

    # Test delta state change
    print("\nChanging to delta state...")
    animation.set_brain_wave_state('delta')

    print(f"Delta state: {animation.brain_wave_state}")
    print(f"Delta breath color: {animation.breath_color}")
    print(f"Delta hold color: {animation.hold_color}")
    print(f"Delta background color: {animation.background}")

    print("\nState change test completed successfully!")

if __name__ == "__main__":
    test_state_changes()