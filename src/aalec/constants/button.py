"""Button constants."""

from micropython import const  # type: ignore


PRESSED: int = const(1)
"""Value of a pressed button."""
RELEASED: int = const(0)
"""Value of a released button."""
SAMPLE_PERIOD: int = const(6)
"""Sample period for debouncing the button in ms."""
