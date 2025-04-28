"""Beeper utilities.

Make sure to connect the jumpers for J4 on the board!
"""

import time

import machine  # type: ignore

from aalec import constants  # type: ignore


class Beeper:
    """Beeper.

    Args:
        pin (int): The pin the beeper is connected to.
    """

    def __init__(self, pin: int):
        self._pin = machine.Pin(pin, machine.Pin.OUT)

    def play(self, freq: int, dur: int | None = None) -> None:
        """Play a tone.

        Args:
            freq (int): The frequency of the tone. If the frequency is <=0, no tone will be played.
            dur (int | None, optional): Duration of the tone in ms.
                If set to `None` the tone will keep playing. Defaults to None.
        """
        pwm = machine.PWM(self._pin, freq=freq, duty_u16=constants.DUTY50)
        if freq <= 0:
            pwm.deinit()
            return
        if dur is not None:
            time.sleep_ms(dur)  # type: ignore
            pwm.deinit()


def test_beeper() -> None:
    """Test for the beeper class."""

    beeper = Beeper(constants.PIN_BEEPER)
    for tone in [
        constants.t_c_1,
        constants.t_d_1,
        constants.t_e_1,
        constants.t_f_1,
        constants.t_g_1,
        constants.t_a_1,
        constants.t_h_1,
        constants.t_off,
    ]:
        beeper.play(tone, 250)
