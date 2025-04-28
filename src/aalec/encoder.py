"""Encoder utility."""

import machine  # type: ignore


class Encoder:
    """Convert encoder value to integer.

    Args:
        track_1 (int): The pin the track_1 of the encoder is connected to.
        track_2 (int): The pin the track_2 of the encoder is connected to.
    """

    def __init__(self, track_1: int, track_2: int) -> None:
        self._pin_track_1 = machine.Pin(track_1, machine.Pin.IN, machine.Pin.PULL_UP)
        self._pin_track_2 = machine.Pin(track_2, machine.Pin.IN, machine.Pin.PULL_UP)

        self._pin_track_1.irq(
            self._encoder_isr, trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING
        )
        self._pin_track_2.irq(
            self._encoder_isr, trigger=machine.Pin.IRQ_FALLING | machine.Pin.IRQ_RISING
        )

        self._z: int = 0
        self._n: int = 0
        self._value: int = 0
        self._old_value: int = 0

    def _encoder_isr(self, _: machine.Pin) -> None:
        """Encoder interrupt service routine."""
        delta: list[list[int]] = [
            [0, 1, 2, 0],
            [0, 1, 0, 3],
            [0, 0, 2, 3],
            [0, 1, 2, 3],
        ]
        transition: list[list[int]] = [
            [0, 1, -1, 0],
            [-1, 0, 0, 1],
            [1, 0, 0, -1],
            [0, -1, 1, 0],
        ]
        state = machine.disable_irq()
        val = (1 - self._pin_track_1.value()) | (1 - self._pin_track_2.value()) << 1
        self._n += transition[self._z][val]
        self._z = delta[self._z][val]
        if self._z == 0:
            if self._n == -4:
                self._value -= 1
            elif self._n == 4:
                self._value += 1
            self._n = 0
        machine.enable_irq(state)

    def get_rotate(self) -> int:
        """Get the rotary encoder value.

        Returns:
            int: Value of the rotary encoder.
        """
        return self._value

    def rotate_changed(self) -> bool:
        """Indicate if the encoder value changed since last call to this method.

        Returns:
            bool: True if the value changed since last call. False otherwise.
        """
        rc: bool = False
        if self._value != self._old_value:
            rc = True
            self._old_value = self._value
        return rc

    def reset_rotate(self, value: int) -> None:
        """Reset rotary encoder value.

        Args:
            value (int): new value for the rotary encoder.
        """
        self._value = value
        self._old_value = value


def test_encoder() -> None:
    """Test for the encoder class."""
    from aalec import constants

    e = Encoder(constants.PIN_ENCODER_TRACK_1, constants.PIN_ENCODER_TRACK_2)
    old_val = e.get_rotate()
    while True:
        val = e.get_rotate()
        if old_val != val:
            print(f"Encoder value: {val}", len(f"{old_val}") * " ", end="\r")
            old_val = val
