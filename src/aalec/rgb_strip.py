"""RGB Strip utilities."""

import machine  # type: ignore
import neopixel  # type: ignore


from aalec import constants


def set_intensity(
    color: constants.RgbColor, intensity: int = constants.MEDIUM
) -> constants.RgbColor:
    """Set the intensity of a color.

    Set the sum of the `r`,`g` and `b` values to `intensity`.

    Args:
        color (RgbColor): Color to balance
        intensity (int, optional): Overall intensity of the color (0 - 786). Defaults to MEDIUM.

    Returns:
        RgbColor: Balanced color.
    """
    color_sum = color.r + color.g + color.b
    if color_sum <= 0 or intensity <= 0:
        return constants.RgbColor(0, 0, 0)

    scale = intensity / color_sum

    return constants.RgbColor(
        int(color.r * scale), int(color.g * scale), int(color.b * scale)
    )


class RgbStrip:
    """Wrapper for neopixel strip.

    Args:
        pin (int): The pin the neopixel strip is connected to.
        n (int): Amount of pixels in the strip. Defaults to `LED_COUNT`.
    """

    def __init__(self, pin: int, n: int = constants.LED_COUNT):
        self._n: int = n
        self._np = neopixel.NeoPixel(machine.Pin(pin), n)
        self._np.fill(constants.c_off)
        self._np.write()

    def set_rgb_led(self, led: int, color: constants.RgbColor) -> None:
        """Set one led of the rgb strip.

        Args:
            led (int): Index of the led in the strip (starts with 0).
            color (RgbColor): The color to set

        Raises:
            AttributeError: If the `led` value does not address a led in the strip.
        """
        if not (0 <= led < self._n):
            raise AttributeError(
                f"You chose an invalid led ({led}). Only values from 0 to {self._n - 1} are allowed."
            )
        self._np[led] = color  # type: ignore
        self._np.write()

    def set_rgb_strip(self, colors: list[constants.RgbColor]) -> None:
        """Set all leds of the rgb strip at once.

        Args:
            colors (list[RgbColor]): A list of colors.

        Raises:
            AttributeError: If the length of the list of colors is not
                exactly the number of leds in the strip.
        """
        if len(colors) != self._n:
            raise AttributeError(
                f"You need to provide a list of exact {self._n} colors"
            )
        for i, color in enumerate(colors):
            self._np[i] = color  # type: ignore
        self._np.write()

    def reset(self) -> None:
        """Reset the strip and turns all leds off."""
        self._np.fill(constants.c_off)
        self._np.write()


def test_rgb_strip():
    """Test for the rgb strip class."""
    from time import sleep

    np = RgbStrip(constants.PIN_RGB_STRIP, constants.LED_COUNT)
    colors = [
        constants.c_off,
        constants.c_red,
        constants.c_green,
        constants.c_blue,
        constants.c_cyan,
        constants.c_purple,
        constants.c_yellow,
        constants.c_white,
    ]
    idx = 0

    try:
        while True:
            for i in range(constants.LED_COUNT):
                np.set_rgb_led(i, colors[(idx + i) % len(colors)])
            idx = (idx + 1) % len(colors)
            sleep(0.5)
    finally:
        np.reset()
