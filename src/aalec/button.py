"""Button Utilities.

Including debouncing of the button.
"""

import machine  # type: ignore

from aalec import constants


class Button:
    """Button class.

    Args:
        button_pin (int): The pin the button of the encoder is connected to.
    """

    def __init__(self, button_pin: int):
        self._pin = machine.Pin(button_pin, machine.Pin.IN, machine.Pin.PULL_UP)
        self._timer = machine.Timer(-1)
        self._timer.init(
            mode=machine.Timer.PERIODIC,
            period=constants.SAMPLE_PERIOD,
            callback=self._debounce_isr,
        )
        self._state: int = 0
        self._value: int = 0
        self._old_value: int = 0

    def get_button(self) -> int:
        """Get the button value.

        Returns:
            int: Value of the button. Button pressed: `1`. Button released: `0`.
        """
        return self._value

    def button_changed(self) -> bool:
        """Indicates if the button value changed since the last call to this method.

        Returns:
            bool: `True` if the value has changed since the last call. `False` otherwise.
        """
        rc = False
        current_value = self.get_button()
        if self._old_value != current_value:
            rc = True
            self._old_value = current_value
        return rc

    def _debounce_isr(self, _: machine.Timer) -> None:
        """Debounce interrupt service routine.

        It works by sampling the pin value every `constants.SAMPLE_PERIOD`.
        If the pin value is stable for at least 12 consecutive calls (0xFFF are 12 bits),
        the button value will be set. Be aware that the value of the pin is inverted.
        """
        self._state = ((self._state << 1) | self._pin.value()) & 0xFFF
        if self._state == 0xFFF:
            self._value = constants.RELEASED
        elif self._state == 0:
            self._value = constants.PRESSED


def test_button() -> None:
    """Test for the Button class."""
    b = Button(constants.PIN_BUTTON)

    print(f"Button value: {b.get_button()}", end="\r")

    while True:
        if b.button_changed():
            print(f"Button value: {b.get_button()}", end="\r")
