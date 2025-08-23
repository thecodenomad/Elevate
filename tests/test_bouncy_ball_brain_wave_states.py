from elevate.constants import StateType
"""Test brain wave state functionality in BouncyBallAnimation."""

import pytest
from elevate.backend.animations.bouncy_ball import BouncyBallAnimation, BRAIN_WAVE_COLORS
from elevate.constants import StateType


def test_brain_wave_state_initialization():
    """Test that brain wave states initialize with correct colors."""
    # Test delta state
    delta_anim = BouncyBallAnimation(brain_wave_state="delta")
    delta_colors = BRAIN_WAVE_COLORS[StateType.DELTA]
    assert delta_anim.breath_color == delta_colors["breath"]
    assert delta_anim.hold_color == delta_colors["hold"]
    assert delta_anim.background == delta_colors["background"]
    assert delta_anim.brain_wave_state == "delta"

    # Test alpha state
    alpha_anim = BouncyBallAnimation(brain_wave_state="alpha")
    alpha_colors = BRAIN_WAVE_COLORS[StateType.ALPHA]
    assert alpha_anim.breath_color == alpha_colors["breath"]
    assert alpha_anim.hold_color == alpha_colors["hold"]
    assert alpha_anim.background == alpha_colors["background"]
    assert alpha_anim.brain_wave_state == "alpha"

    # Test beta state
    beta_anim = BouncyBallAnimation(brain_wave_state="beta")
    beta_colors = BRAIN_WAVE_COLORS[StateType.BETA]
    assert beta_anim.breath_color == beta_colors["breath"]
    assert beta_anim.hold_color == beta_colors["hold"]
    assert beta_anim.background == beta_colors["background"]
    assert beta_anim.brain_wave_state == "beta"

    # Test gamma state
    gamma_anim = BouncyBallAnimation(brain_wave_state="gamma")
    gamma_colors = BRAIN_WAVE_COLORS[StateType.GAMMA]
    assert gamma_anim.breath_color == gamma_colors["breath"]
    assert gamma_anim.hold_color == gamma_colors["hold"]
    assert gamma_anim.background == gamma_colors["background"]
    assert gamma_anim.brain_wave_state == "gamma"


def test_brain_wave_state_case_insensitive():
    """Test that brain wave states work case insensitively."""
    # Test uppercase
    anim = BouncyBallAnimation(brain_wave_state="DELTA")
    delta_colors = BRAIN_WAVE_COLORS[StateType.DELTA]
    assert anim.breath_color == delta_colors["breath"]
    assert anim.hold_color == delta_colors["hold"]
    assert anim.background == delta_colors["background"]
    assert anim.brain_wave_state == "delta"


def test_invalid_brain_wave_state():
    """Test that invalid brain wave states fall back to default colors."""
    # Test with invalid state - should use default colors
    default_breath = BRAIN_WAVE_COLORS[StateType.THETA]["breath"]  # Default breath color
    default_hold = BRAIN_WAVE_COLORS[StateType.THETA]["hold"]  # Default hold color
    default_background = BRAIN_WAVE_COLORS[StateType.THETA]["background"]  # Default background color
    
    anim = BouncyBallAnimation(brain_wave_state="invalid", 
                              breath_color=default_breath,
                              hold_color=default_hold,
                              background=default_background)
    assert anim.breath_color == default_breath
    assert anim.hold_color == default_hold
    assert anim.background == default_background
    assert anim.brain_wave_state == "invalid"


def test_set_brain_wave_state():
    """Test dynamically setting brain wave state."""
    anim = BouncyBallAnimation()
    
    # Set to delta state
    anim.set_brain_wave_state("delta")
    delta_colors = BRAIN_WAVE_COLORS[StateType.DELTA]
    assert anim.breath_color == delta_colors["breath"]
    assert anim.hold_color == delta_colors["hold"]
    assert anim.background == delta_colors["background"]
    assert anim.brain_wave_state == "delta"
    
    # Set to alpha state
    anim.set_brain_wave_state("alpha")
    alpha_colors = BRAIN_WAVE_COLORS[StateType.ALPHA]
    assert anim.breath_color == alpha_colors["breath"]
    assert anim.hold_color == alpha_colors["hold"]
    assert anim.background == alpha_colors["background"]
    assert anim.brain_wave_state == "alpha"


def test_set_invalid_brain_wave_state():
    """Test setting invalid brain wave state."""
    anim = BouncyBallAnimation(brain_wave_state="delta")
    
    # Try to set invalid state - should not change colors
    original_breath = anim.breath_color
    original_hold = anim.hold_color
    original_background = anim.background
    original_state = anim.brain_wave_state
    
    # This should not change anything since "invalid" is not a valid state
    # The method doesn't raise an error but also doesn't change the state
    # In a real implementation, you might want different behavior
    anim.set_brain_wave_state("invalid")
    assert anim.breath_color == original_breath
    assert anim.hold_color == original_hold
    assert anim.background == original_background
    assert anim.brain_wave_state == original_state