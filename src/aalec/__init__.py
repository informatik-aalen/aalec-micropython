"""AALeC library implementation.

This class tries to implement the same API as the arduino version of this library.
The original implementation can be found here: [AALeC-V3](https://github.com/informatik-aalen/AALeC-V3).

Attention:
    Some changes:

    - This library works only for the BMP280 environment sensor.
    - The Wii-Nunchuck controller is not implemented.

"""

import machine  # type: ignore

from aalec import beeper, button, constants, display, encoder, environment, rgb_strip

__all__ = ["constants", "AALeC"]


class AALeC:
    """Proxy class to implement the AALeC API."""

    def __init__(self):
        self._adc = machine.ADC(0)
        self._beeper = beeper.Beeper(constants.PIN_BEEPER)
        self._button = button.Button(constants.PIN_BUTTON)
        self._i2c = machine.I2C(
            sda=machine.Pin(constants.PIN_SDA), scl=machine.Pin(constants.PIN_SCL)
        )
        self._display = display.Display(self._i2c)
        self._encoder = encoder.Encoder(
            constants.PIN_ENCODER_TRACK_1, constants.PIN_ENCODER_TRACK_2
        )
        self._environment = environment.Environment(self._i2c, constants.BMP280_ADDR)
        self._rgb_strip = rgb_strip.RgbStrip(
            constants.PIN_RGB_STRIP, constants.LED_COUNT
        )

    def id(self) -> str:
        """A unique ID for this board.

        Returns:
            str: The unique ID for this board.
        """
        # Calculate the ID just like ESP.getChipId() in Arduino.
        chip_id = machine.unique_id()
        chip_id_int = int.from_bytes(chip_id[-3:], "big")

        return f"AALeC-{chip_id_int}"

    def get_analog(self) -> int:
        """Get value from analog pin.

        Returns:
            int: Value of the 10 bit ADC (0-1024)
        """
        return self._adc.read()

    def play(self, freq: int, dur: int | None = None) -> None:
        """Proxy for [`Beeper.play`](beeper.md#aalec.beeper.Beeper.play).

        Args:
            freq (int): The frequency of the tone. If the frequency is <=0, no tone will be played.
            dur (int | None, optional): Duration of the tone in ms.
                If set to `None` the tone will keep playing. Defaults to None.
        """
        self._beeper.play(freq, dur)

    def get_button(self) -> int:
        """Proxy for [`Button.get_button`](button.md#aalec.button.Button.get_button).

        Returns:
            int: Value of the button. Button pressed: `1`. Button released: `0`.
        """
        return self._button.get_button()

    def button_changed(self) -> bool:
        """Proxy for [`Button.button_change`](button.md#aalec.button.Button.button_changed).

        Returns:
            bool: `True` if the value has changed since the last call. `False` otherwise.
        """
        return self._button.button_changed()

    def print_line(self, line: int, text: str) -> None:
        """Proxy for [`Display.print_line`](display.md#aalec.display.Display.print_line).

        A line can be at most 16 characters long. (A character has a size of 8x8 pixels.)

        Args:
            line (int): Line number. Valid values are from 1 to 5.
            text (str): The content to display.
        """
        self._display.print_line(line, text)

    def clear_display(self) -> None:
        """Proxy for [`Display.clear_display`](display.md#aalec.display.Display.clear_display)."""
        self._display.clear_display()

    def rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """Proxy for [`Display.rect`](display.md#aalec.display.Display.rect).

        Args:
            x (int): X coordinate of the upper left corner of the progressbar
            y (int): Y coordinate of the upper left corner of the progressbar
            width (int): Width of the progressbar in pixel. (x delta to the lower right corner.)
            height (int): Height of the progressbar in pixel. (y delta to the lower right corner.)
            color (int): Frame color (`constants.WHITE` or `constants.BLACK`)
        """
        self._display.rect(x, y, width, height, color)

    def filled_rect(self, x: int, y: int, width: int, height: int, color: int) -> None:
        """Proxy for [`Display.filled_rect`](display.md#aalec.display.Display.filled_rect).

        Args:
            x (int): X coordinate of the upper left corner of the progressbar
            y (int): Y coordinate of the upper left corner of the progressbar
            width (int): Width of the progressbar in pixel. (x delta to the lower right corner.)
            height (int): Height of the progressbar in pixel. (y delta to the lower right corner.)
            color (int): Fill color (`constants.WHITE` or `constants.BLACK`)
        """
        self._display.filled_rect(x, y, width, height, color)

    def draw_progressbar(
        self, x: int, y: int, width: int, height: int, percent: int
    ) -> None:
        """Proxy for [`Display.draw_progressbar`](display.md#aalec.display.Display.draw_progressbar).

        Args:
            x (int): X coordinate of the upper left corner of the progressbar
            y (int): Y coordinate of the upper left corner of the progressbar
            width (int): Width of the progressbar in pixel. (x delta to the lower right corner.)
            height (int): Height of the progressbar in pixel. (y delta to the lower right corner.)
            percent (int): How many percent the bar is filled (grows to the right).
        """
        self._display.draw_progressbar(x, y, width, height, percent)

    def get_rotate(self) -> int:
        """Proxy for [`Encoder.get_rotate`](encoder.md#aalec.encoder.Encoder.get_rotate).

        Returns:
            int: Value of the rotary encoder.
        """
        return self._encoder.get_rotate()

    def rotate_changed(self) -> bool:
        """Proxy for [`Encoder.rotate_changed`](encoder.md#aalec.encoder.Encoder.rotate_changed).

        Returns:
            bool: True if the value changed since last call. False otherwise.
        """
        return self._encoder.rotate_changed()

    def reset_rotate(self, value: int) -> None:
        """Proxy for [`Encoder.reset_rotate`](encoder.md#aalec.encoder.Encoder.reset_rotate).

        Args:
            value (int): new value for the rotary encoder.
        """
        self._encoder.reset_rotate(value)

    def get_environment_sensor(self) -> str:
        """Proxy for [`Environment.get_environment_sensor`](environment.md#aalec.environment.Environment.get_environment_sensor).

        Returns:
            str: "BMP280"
        """
        return self._environment.get_environment_sensor()

    def get_temp(self) -> float:
        """Proxy for [`Environment.get_temp`](environment.md#aalec.environment.Environment.get_temp).

        Returns:
            float: Current temperature in °C.
        """
        return self._environment.get_temp()

    def get_humidity(self) -> float:
        """Proxy for [`Environment.get_humidity`](environment.md#aalec.environment.Environment.get_humidity).

        Returns:
            float: 0.0 (BMP280 doesn't have a humidity sensor).
        """
        return self._environment.get_humidity()

    def get_pressure(self) -> float:
        """Proxy for [`Environment.get_pressure`](environment.md#aalec.environment.Environment.get_pressure).

        Returns:
            float: current pressure in hPa.
        """
        return self._environment.get_pressure()

    def get_gas_resistance(self) -> float:
        """Proxy for [`Environment.get_gas_resistance`](environment.md#aalec.environment.Environment.get_gas_resistance).

        Returns:
            float: 0.0 (BMP280 doesn't have a gas resistance sensor).
        """
        return self._environment.get_gas_resistance()

    def set_rgb_led(self, led: int, color: constants.RgbColor) -> None:
        """Proxy for [`RgbStrip.set_rgb_led`](rgb_strip.md#aalec.rgb_strip.RgbStrip.set_rgb_led).

        Args:
            led (int): Index of the led in the strip (starts with 0).
            color (RgbColor): The color to set

        Raises:
            AttributeError: If the `led` value does not address a led in the strip.
        """
        self._rgb_strip.set_rgb_led(led, color)

    def set_rgb_strip(self, colors: list[constants.RgbColor]) -> None:
        """Proxy for [`RgbStrip.set_rgb_strip`](rgb_strip.md#aalec.rgb_strip.RgbStrip.set_rgb_strip).

        Args:
            colors (list[RgbColor]): A list of colors.

        Raises:
            AttributeError: If the length of the list of colors is not
                exactly the number of leds in the strip.
        """
        self._rgb_strip.set_rgb_strip(colors)

    def reset_rgb_strip(self) -> None:
        """Proxy for [`RgbStrip.reset`](rgb_strip.md#aalec.rgb_strip.RgbStrip.reset)."""
        self._rgb_strip.reset()
