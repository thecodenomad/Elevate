"""Base classes and protocols for animations.

This module defines the base animation class and protocol interfaces
used by all animation implementations in the Elevate application.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Protocol, Tuple


class CairoContext(Protocol):
    """Protocol defining the Cairo context interface for drawing operations.

    This protocol specifies the methods that animation classes can use
    to draw on a Cairo context. It includes basic drawing operations
    like setting colors, drawing shapes, and rendering text.
    """

    def set_source_rgb(self, r: float, g: float, b: float) -> None:
        """Set the source pattern to a solid color.

        Args:
            r (float): Red component (0.0 to 1.0)
            g (float): Green component (0.0 to 1.0)
            b (float): Blue component (0.0 to 1.0)
        """

    def rectangle(self, x: float, y: float, w: float, h: float) -> None:
        """Add a rectangle to the current path.

        Args:
            x (float): X coordinate of the top-left corner
            y (float): Y coordinate of the top-left corner
            w (float): Width of the rectangle
            h (float): Height of the rectangle
        """

    def fill(self) -> None:
        """Fill the current path with the current source pattern."""

    def arc(self, xc: float, yc: float, radius: float, angle1: float, angle2: float) -> None:
        """Add a circular arc to the current path.

        Args:
            xc (float): X coordinate of the center
            yc (float): Y coordinate of the center
            radius (float): Radius of the arc
            angle1 (float): Starting angle in radians
            angle2 (float): Ending angle in radians
        """

    def paint(self) -> None:
        """Fill the current clip region with the current source pattern."""

    def select_font_face(self, family: str, slant: int, weight: int) -> None:
        """Select a font family for text rendering.

        Args:
            family (str): Font family name
            slant (int): Font slant (cairo.FONT_SLANT_*)
            weight (int): Font weight (cairo.FONT_WEIGHT_*)
        """

    def set_font_size(self, size: float) -> None:
        """Set the font size for text rendering.

        Args:
            size (float): Font size in points
        """

    def text_extents(self, text: str) -> Tuple[float, float, float, float, float, float]:
        """Get the extents of a text string.

        Args:
            text (str): Text string to measure

        Returns:
            Tuple[float, float, float, float, float, float]: Text extents as
                (x_bearing, y_bearing, width, height, x_advance, y_advance)
        """

    def move_to(self, x: float, y: float) -> None:
        """Move the current point to the specified coordinates.

        Args:
            x (float): X coordinate
            y (float): Y coordinate
        """

    def show_text(self, text: str) -> None:
        """Draw a text string at the current point.

        Args:
            text (str): Text string to draw
        """


class Animation(ABC):
    """Abstract base class for all animation implementations.

    This class defines the interface that all animation classes must implement.
    Concrete animation classes should inherit from this class and implement
    all abstract methods.
    """

    @abstractmethod
    def reset(self) -> None:
        """Reset the animation to its initial state.

        This method should initialize or reinitialize any animation state
        variables to their starting values.
        """

    def set_breath_cycle(self, cycle: Tuple[float, float, float, float]) -> None:
        """Set the breath cycle parameters for breathing animations.

        Args:
            cycle (Tuple[float, float, float, float]): Breath cycle parameters as
                (inhale, hold, exhale, hold) in seconds
        """

    @abstractmethod
    def update(self, dt: float, width: int, height: int) -> None:
        """Update the animation state based on elapsed time.

        This method is called periodically to update the animation's
        internal state variables based on the time elapsed since the
        last update.

        Args:
            dt (float): Time elapsed since last update in seconds
            width (int): Current width of the drawing area
            height (int): Current height of the drawing area
        """

    @abstractmethod
    def render(self, cr: CairoContext, width: int, height: int, now_s: float) -> None:
        """Render the animation frame using the Cairo context.

        This method is responsible for drawing the current frame of the
        animation using the provided Cairo context.

        Args:
            cr (CairoContext): Cairo context for drawing operations
            width (int): Width of the drawing area
            height (int): Height of the drawing area
            now_s (float): Current time in seconds for animation calculations
        """
