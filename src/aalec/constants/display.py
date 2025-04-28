"""Display constants."""

from micropython import const  # type: ignore

BLACK: int = const(0)
"""Display color Black."""
WHITE: int = const(1)
"""Display color White."""

DISPLAY_WIDTH: int = const(128)
"""Width of the display in pixel."""
DISPLAY_HEIGHT: int = const(64)
"""Height of the display in pixel."""
LINE_HEIGHT: int = const(12)
"""Height of a text line on the display in pixel."""
MAX_LINE_COUNT: int = const(5)
"""Number of text lines on the display."""
