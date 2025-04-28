"""RGB Strip constants."""

import collections

from micropython import const  # type: ignore


class RgbColor(collections.namedtuple("RgbColorBase", ["r", "g", "b"])):
    """RGB Color.

    Attributes:
        r (int): red part of the color. (0-255)
        g (int): green part of the color. (0-255)
        b (int): blue part of the color. (0-255)
    """

    __slots__ = ()


LED_COUNT: int = const(5)
"""The amount of leds in the strip on the AALeC."""

DIM: int = const(50)
"""Dim intensity of a color."""
MEDIUM: int = const(100)
"""Medium intensity of a color."""
BRIGHT: int = const(200)
"""Bright intensity of a color."""

c_off: RgbColor = RgbColor(0, 0, 0)
"""Led Off"""
c_red: RgbColor = RgbColor(100, 0, 0)
"""Red color (medium brightness)"""
c_green: RgbColor = RgbColor(0, 100, 0)
"""Green color (medium brightness)"""
c_blue: RgbColor = RgbColor(0, 0, 100)
"""Blue color (medium brightness)"""
c_yellow: RgbColor = RgbColor(50, 50, 0)
"""Yellow color (medium brightness)"""
c_white: RgbColor = RgbColor(33, 33, 33)
"""White color (medium brightness)"""
c_cyan: RgbColor = RgbColor(0, 50, 50)
"""Cyan color (medium brightness)"""
c_purple: RgbColor = RgbColor(50, 0, 50)
"""Purple color (medium brightness)"""
