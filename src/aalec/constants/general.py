"""Global constants."""

from micropython import const  # type: ignore

PIN_BUTTON: int = const(0)
"""Pin number of the button in the rotary encoder."""
PIN_ADC: int = const(0)
"""Pin number of the adc pin (not physically the same pin as the button!)"""
PIN_TX: int = const(1)
"""Pin number of the TX port."""
PIN_RGB_STRIP: int = const(2)
"""Pin number of the rgb strip."""
PIN_RX: int = const(3)
"""Pin number of the RX port."""
PIN_SDA: int = const(4)
"""Pin number of the sda port for i2c."""
PIN_SCL: int = const(5)
"""Pin number of the scl port for i2c."""
PIN_ENCODER_TRACK_1: int = const(12)
"""Pin number of the first track of the encoder."""
PIN_ENCODER_TRACK_2: int = const(14)
"""Pin number of the second track of the encoder."""
PIN_BEEPER: int = const(15)
"""Pin number of the beeper."""
